"""
MaskDNS - Domain Masking Service
A Flask application that masks free subdomains behind custom domains
"""
import os
import sqlite3
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs
from functools import wraps
import hashlib

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
import requests

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Ensure database directory exists
db_path = os.environ.get('DATABASE_PATH', 'domains.db')
db_dir = os.path.dirname(db_path)
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)

app.config['DATABASE'] = db_path
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'admin123')
app.config['TIMEOUT'] = int(os.environ.get('TIMEOUT', '30'))

# Database initialization
def init_db():
    """Initialize SQLite database with required tables"""
    # Ensure database directory exists
    db_path = app.config['DATABASE']
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS domain_mappings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                custom_domain TEXT UNIQUE NOT NULL,
                target_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                clicks INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()
        print(f"Database initialized successfully at {db_path}")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

def get_db():
    """Get database connection"""
    # Ensure database is initialized
    db_path = app.config['DATABASE']
    if not os.path.exists(db_path):
        init_db()
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Verify table exists, create if missing
    try:
        conn.execute("SELECT 1 FROM domain_mappings LIMIT 1")
    except sqlite3.OperationalError:
        conn.close()
        init_db()
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
    
    return conn

def login_required(f):
    """Decorator for admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def clean_domain(domain):
    """Extract clean domain from URL or hostname"""
    domain = domain.strip().lower()
    domain = domain.replace('http://', '').replace('https://', '')
    domain = domain.split('/')[0]
    return domain

def validate_url(url):
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False

def track_click(domain_id):
    """Increment click counter for domain mapping"""
    conn = get_db()
    conn.execute('UPDATE domain_mappings SET clicks = clicks + 1 WHERE id = ?', (domain_id,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == app.config['ADMIN_PASSWORD']:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        return render_template('login.html', error='Invalid password')
    return render_template('login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_panel():
    """Admin panel - list all domain mappings"""
    conn = get_db()
    mappings = conn.execute('SELECT * FROM domain_mappings ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('admin.html', mappings=mappings)

@app.route('/admin/add', methods=['POST'])
@login_required
def add_mapping():
    """Add new domain mapping"""
    custom_domain = request.form.get('custom_domain', '').strip()
    target_url = request.form.get('target_url', '').strip()
    
    # Validate inputs
    if not custom_domain or not target_url:
        return jsonify({'success': False, 'error': 'All fields required'}), 400
    
    custom_domain = clean_domain(custom_domain)
    
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'https://' + target_url
    
    if not validate_url(target_url):
        return jsonify({'success': False, 'error': 'Invalid target URL'}), 400
    
    try:
        conn = get_db()
        conn.execute(
            'INSERT INTO domain_mappings (custom_domain, target_url) VALUES (?, ?)',
            (custom_domain, target_url)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('admin_panel'))
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Domain already exists'}), 400

@app.route('/admin/delete/<int:mapping_id>', methods=['POST'])
@login_required
def delete_mapping(mapping_id):
    """Delete domain mapping"""
    conn = get_db()
    conn.execute('DELETE FROM domain_mappings WHERE id = ?', (mapping_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/admin/toggle/<int:mapping_id>', methods=['POST'])
@login_required
def toggle_mapping(mapping_id):
    """Toggle active status of domain mapping"""
    conn = get_db()
    conn.execute('UPDATE domain_mappings SET is_active = NOT is_active WHERE id = ?', (mapping_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/stats/<domain>')
def view_stats(domain):
    """View statistics for a specific domain"""
    domain = clean_domain(domain)
    conn = get_db()
    mapping = conn.execute(
        'SELECT * FROM domain_mappings WHERE custom_domain = ?',
        (domain,)
    ).fetchone()
    conn.close()
    
    if mapping:
        return render_template('stats.html', mapping=dict(mapping))
    return render_template('error.html', message='Domain not found'), 404

@app.route('/<path:path>')
@app.route('/proxy', defaults={'path': ''})
def proxy_handler(path):
    """Main proxy handler - fetches content from target URL"""
    host = request.headers.get('Host', request.host).split(':')[0]
    
    # Look up domain mapping
    conn = get_db()
    mapping = conn.execute(
        'SELECT * FROM domain_mappings WHERE custom_domain = ? AND is_active = 1',
        (host,)
    ).fetchone()
    conn.close()
    
    if not mapping:
        return render_template('not_configured.html', domain=host), 404
    
    # Track click
    track_click(mapping['id'])
    
    # Build target URL
    target_url = mapping['target_url'].rstrip('/')
    if path:
        target_url = f"{target_url}/{path}"
    
    # Add query parameters
    if request.query_string:
        target_url = f"{target_url}?{request.query_string.decode()}"
    
    try:
        # Prepare headers
        headers = {
            'User-Agent': request.headers.get('User-Agent', 'MaskDNS/1.0'),
            'Accept': request.headers.get('Accept', '*/*'),
            'Accept-Language': request.headers.get('Accept-Language', 'en-US,en;q=0.9'),
        }
        
        # Fetch content from target
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=app.config['TIMEOUT'],
            stream=True
        )
        
        # Handle redirects
        if response.status_code in [301, 302, 303, 307, 308]:
            location = response.headers.get('Location', '')
            if location.startswith('/'):
                # Relative redirect - keep on our domain
                return redirect(location, code=response.status_code)
            else:
                # Absolute redirect - proxy it
                return redirect(location, code=response.status_code)
        
        # Build response
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = [
            (name, value) for (name, value) in response.raw.headers.items()
            if name.lower() not in excluded_headers
        ]
        
        return Response(
            response.content,
            status=response.status_code,
            headers=response_headers
        )
        
    except requests.exceptions.Timeout:
        return render_template('error.html', message='Target URL timeout'), 504
    except requests.exceptions.RequestException as e:
        return render_template('error.html', message=f'Error fetching target: {str(e)}'), 502
    except Exception as e:
        return render_template('error.html', message='Internal server error'), 500

@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    return render_template('error.html', message='Page not found'), 404

@app.errorhandler(500)
def server_error(e):
    """500 error handler"""
    return render_template('error.html', message='Internal server error'), 500

# Initialize database on import (for gunicorn)
init_db()

if __name__ == '__main__':
    app.run(debug=os.environ.get('DEBUG', 'False') == 'True', host='0.0.0.0', port=5000)
