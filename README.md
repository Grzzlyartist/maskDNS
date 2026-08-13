# 🔗 MaskDNS - Free Domain Masking Service

A complete Python web application that masks free subdomains (Vercel, Netlify, Heroku, etc.) behind custom domains. Built with Flask, SQLite, and designed for 100% free deployment.

## 🚀 Features

- **Domain Masking**: Hide free subdomains behind branded domains
- **Admin Panel**: Password-protected CRUD interface
- **Click Tracking**: Monitor traffic and analytics
- **Active/Inactive Toggle**: Enable/disable mappings instantly
- **Responsive UI**: Works on desktop, tablet, and mobile
- **Error Handling**: Proper error pages and timeout handling
- **100% Free**: No paid services required

## 📦 Installation

### Local Setup

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

4. **Access the application**:
- Landing page: `http://localhost:5000`
- Admin panel: `http://localhost:5000/admin/login`
- Default password: `admin123`

### Environment Variables

Create a `.env` file or set these environment variables:

```env
ADMIN_PASSWORD=your-secure-password
SECRET_KEY=your-flask-secret-key
DEBUG=False
DATABASE_PATH=/path/to/domains.db
TIMEOUT=30
```

## 🌐 Deployment Guides

### Option 1: PythonAnywhere (FREE)

1. **Create account**: Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload files**:
   - Go to Files tab
   - Upload all project files
   - Or use git: `git clone your-repo-url`

3. **Install dependencies**:
   - Open Bash console
   - Run: `pip3 install --user -r requirements.txt`

4. **Configure Web App**:
   - Go to Web tab → Add new web app
   - Choose Flask
   - Python version: 3.10
   - Set source code path: `/home/yourusername/maskdns`
   - Set working directory: `/home/yourusername/maskdns`

5. **Edit WSGI file** (`/var/www/yourusername_pythonanywhere_com_wsgi.py`):
```python
import sys
path = '/home/yourusername/maskdns'
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application
```

6. **Set environment variables**:
   - In Web tab, scroll to Environment Variables
   - Add: `ADMIN_PASSWORD=your-password`

7. **Initialize database**:
   - Open Bash console
   - Navigate to project directory
   - Run: `python3 -c "from app import init_db; init_db()"`

8. **Reload**: Click green reload button

### Option 2: Render (FREE)

1. **Create account**: Sign up at [render.com](https://render.com)

2. **Create new Web Service**:
   - Connect your GitHub repository
   - Or use this repository

3. **Configure service**:
   - **Name**: maskdns
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. **Add environment variables**:
   - `ADMIN_PASSWORD` = your-secure-password
   - `SECRET_KEY` = your-secret-key

5. **Deploy**: Click Create Web Service

### Option 3: Fly.io (FREE)

1. **Install Fly CLI**:
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Login**:
```bash
fly auth login
```

3. **Create `fly.toml`** (already included):
```toml
app = "maskdns"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

4. **Deploy**:
```bash
fly launch
fly secrets set ADMIN_PASSWORD=your-password
fly deploy
```

## 🔧 DNS Configuration

### Step 1: Point Domain to Server

Add an **A Record** in your domain's DNS settings:

```
Type: A
Name: app (or your subdomain)
Value: YOUR_SERVER_IP
TTL: 300
```

**Examples**:
- PythonAnywhere: Find IP via `ping yourusername.pythonanywhere.com`
- Render: Use the IP from your service dashboard
- Fly.io: Use `fly ips list`

### Step 2: Wait for DNS Propagation

DNS changes take 5-30 minutes to propagate. Check status:
```bash
nslookup app.yourdomain.com
```

### Step 3: Add Mapping in Admin Panel

1. Go to admin panel
2. Enter custom domain: `app.yourdomain.com`
3. Enter target URL: `https://yourapp.vercel.app`
4. Click Add Mapping

### Step 4: Test

Visit `http://app.yourdomain.com` - you should see content from your target URL!

## 🆓 Free Domain Options

### DuckDNS (Free Subdomain)

1. Sign up at [duckdns.org](https://www.duckdns.org)
2. Create subdomain: `yourapp.duckdns.org`
3. Point to your server IP
4. Use in MaskDNS admin panel

### Freenom (Free TLDs)

1. Sign up at [freenom.com](https://www.freenom.com)
2. Search for available `.tk`, `.ml`, `.ga`, `.cf`, or `.gq` domains
3. Register for free (12 months)
4. Configure DNS in management panel

### Cloudflare (Free SSL)

1. Sign up at [cloudflare.com](https://www.cloudflare.com)
2. Add your domain
3. Update nameservers at your registrar
4. Enable SSL/TLS (Full mode)
5. Enable "Always Use HTTPS"

## 📊 Usage Example

### Before MaskDNS:
```
Your site: https://my-cool-app-xyz123.vercel.app
Problem: Long, unmemorable, not branded
```

### After MaskDNS:
```
Your custom domain: https://app.mybrand.com
Benefits: Short, branded, professional
Visitors see: app.mybrand.com (target URL is hidden!)
```

### Real-World Flow:

1. **You deploy** to Vercel: `my-portfolio.vercel.app`
2. **You own domain**: `johndoe.com`
3. **You setup DNS**: `portfolio.johndoe.com → A → SERVER_IP`
4. **You add mapping**: `portfolio.johndoe.com` → `my-portfolio.vercel.app`
5. **Visitors access**: `portfolio.johndoe.com` (sees Vercel content, URL stays the same!)

## 🔒 Security Best Practices

1. **Change default password**:
   - Set `ADMIN_PASSWORD` environment variable
   - Use strong, unique password

2. **Use HTTPS**:
   - Enable SSL on hosting platform
   - Use Cloudflare for free SSL

3. **Rate limiting** (optional):
   - Use Cloudflare rate limiting
   - Or implement Flask-Limiter

4. **Backup database**:
```bash
cp domains.db domains.db.backup
```

5. **Monitor logs**:
   - Check platform logs regularly
   - Set up error notifications

## 🛠️ Troubleshooting

### Domain not working?

1. **Check DNS**: `nslookup your-domain.com`
2. **Check mapping**: Go to admin panel, verify domain is active
3. **Check target URL**: Make sure target site is accessible
4. **Check logs**: View application logs on hosting platform

### 404 Error?

- Domain not configured in admin panel
- Domain spelling mismatch
- Mapping is inactive

### 502 Bad Gateway?

- Target URL is down or unreachable
- Timeout (increase `TIMEOUT` env var)
- Target URL blocks proxy requests

### Admin password not working?

- Check `ADMIN_PASSWORD` environment variable
- Restart application after changing env vars

## 📝 Database Schema

```sql
CREATE TABLE domain_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    custom_domain TEXT UNIQUE NOT NULL,
    target_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    clicks INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1
);
```

## 🎯 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Landing page |
| GET | `/admin/login` | Admin login |
| POST | `/admin/login` | Submit login |
| GET | `/admin` | Admin panel |
| POST | `/admin/add` | Create mapping |
| POST | `/admin/delete/<id>` | Delete mapping |
| POST | `/admin/toggle/<id>` | Toggle active status |
| GET | `/stats/<domain>` | View statistics |
| GET | `/<path:path>` | Proxy handler |

## 🤝 Contributing

Feel free to submit issues and pull requests!

## 📄 License

MIT License - feel free to use for any purpose!

## 🙏 Credits

Built with:
- Flask - Web framework
- Requests - HTTP library
- SQLite - Database

## 📧 Support

For issues or questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review troubleshooting section above

---

**Made with ❤️ for the developer community**

🎉 **Enjoy your free domain masking service!**
