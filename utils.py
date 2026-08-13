"""
Utility functions for MaskDNS
Command-line tools for database management
"""
import sqlite3
import sys
from datetime import datetime

DATABASE = 'domains.db'

def list_mappings():
    """List all domain mappings"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    mappings = conn.execute('SELECT * FROM domain_mappings ORDER BY created_at DESC').fetchall()
    conn.close()
    
    if not mappings:
        print("No domain mappings found.")
        return
    
    print("\n" + "="*80)
    print(f"{'ID':<5} {'Custom Domain':<30} {'Clicks':<10} {'Active':<10}")
    print("="*80)
    
    for mapping in mappings:
        active = "✓ Yes" if mapping['is_active'] else "✗ No"
        print(f"{mapping['id']:<5} {mapping['custom_domain']:<30} {mapping['clicks']:<10} {active:<10}")
    
    print("="*80)
    print(f"\nTotal mappings: {len(mappings)}")

def add_mapping_cli(custom_domain, target_url):
    """Add a new domain mapping via CLI"""
    try:
        conn = sqlite3.connect(DATABASE)
        conn.execute(
            'INSERT INTO domain_mappings (custom_domain, target_url) VALUES (?, ?)',
            (custom_domain, target_url)
        )
        conn.commit()
        conn.close()
        print(f"✓ Successfully added mapping: {custom_domain} → {target_url}")
        return True
    except sqlite3.IntegrityError:
        print(f"✗ Error: Domain '{custom_domain}' already exists")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def delete_mapping_cli(domain):
    """Delete a domain mapping via CLI"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.execute('DELETE FROM domain_mappings WHERE custom_domain = ?', (domain,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    
    if rows_affected > 0:
        print(f"✓ Successfully deleted mapping for: {domain}")
        return True
    else:
        print(f"✗ Error: Domain '{domain}' not found")
        return False

def toggle_mapping_cli(domain):
    """Toggle active status of a domain mapping via CLI"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    
    # Get current status
    mapping = conn.execute('SELECT * FROM domain_mappings WHERE custom_domain = ?', (domain,)).fetchone()
    
    if not mapping:
        print(f"✗ Error: Domain '{domain}' not found")
        conn.close()
        return False
    
    # Toggle status
    new_status = not mapping['is_active']
    conn.execute('UPDATE domain_mappings SET is_active = ? WHERE custom_domain = ?', (new_status, domain))
    conn.commit()
    conn.close()
    
    status_text = "activated" if new_status else "deactivated"
    print(f"✓ Successfully {status_text}: {domain}")
    return True

def export_mappings(filename='mappings_export.csv'):
    """Export all mappings to CSV"""
    import csv
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    mappings = conn.execute('SELECT * FROM domain_mappings').fetchall()
    conn.close()
    
    if not mappings:
        print("No mappings to export.")
        return False
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Custom Domain', 'Target URL', 'Created At', 'Clicks', 'Active'])
        
        for mapping in mappings:
            writer.writerow([
                mapping['id'],
                mapping['custom_domain'],
                mapping['target_url'],
                mapping['created_at'],
                mapping['clicks'],
                mapping['is_active']
            ])
    
    print(f"✓ Exported {len(mappings)} mappings to {filename}")
    return True

def backup_database(backup_file=None):
    """Backup the database"""
    import shutil
    
    if backup_file is None:
        backup_file = f"domains_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    
    try:
        shutil.copy2(DATABASE, backup_file)
        print(f"✓ Database backed up to: {backup_file}")
        return True
    except Exception as e:
        print(f"✗ Backup failed: {str(e)}")
        return False

def reset_clicks(domain=None):
    """Reset click counter for a domain or all domains"""
    conn = sqlite3.connect(DATABASE)
    
    if domain:
        cursor = conn.execute('UPDATE domain_mappings SET clicks = 0 WHERE custom_domain = ?', (domain,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        if rows_affected > 0:
            print(f"✓ Reset clicks for: {domain}")
            return True
        else:
            print(f"✗ Domain not found: {domain}")
            return False
    else:
        conn.execute('UPDATE domain_mappings SET clicks = 0')
        conn.commit()
        conn.close()
        print("✓ Reset clicks for all domains")
        return True

def show_stats(domain):
    """Show detailed statistics for a domain"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    mapping = conn.execute('SELECT * FROM domain_mappings WHERE custom_domain = ?', (domain,)).fetchone()
    conn.close()
    
    if not mapping:
        print(f"✗ Domain not found: {domain}")
        return False
    
    print("\n" + "="*60)
    print(f"Statistics for: {domain}")
    print("="*60)
    print(f"Target URL: {mapping['target_url']}")
    print(f"Total Clicks: {mapping['clicks']}")
    print(f"Status: {'✓ Active' if mapping['is_active'] else '✗ Inactive'}")
    print(f"Created: {mapping['created_at']}")
    print("="*60)
    return True

def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("\nMaskDNS Utility Tools")
        print("="*60)
        print("Usage: python utils.py <command> [options]")
        print("\nCommands:")
        print("  list                          - List all mappings")
        print("  add <domain> <target_url>     - Add new mapping")
        print("  delete <domain>               - Delete mapping")
        print("  toggle <domain>               - Toggle active status")
        print("  stats <domain>                - Show statistics")
        print("  export [filename]             - Export to CSV")
        print("  backup [filename]             - Backup database")
        print("  reset-clicks [domain]         - Reset click counter")
        print("\nExamples:")
        print("  python utils.py list")
        print("  python utils.py add app.example.com https://myapp.vercel.app")
        print("  python utils.py delete app.example.com")
        print("  python utils.py stats app.example.com")
        print("="*60)
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_mappings()
    
    elif command == 'add':
        if len(sys.argv) < 4:
            print("Usage: python utils.py add <domain> <target_url>")
            return
        add_mapping_cli(sys.argv[2], sys.argv[3])
    
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Usage: python utils.py delete <domain>")
            return
        delete_mapping_cli(sys.argv[2])
    
    elif command == 'toggle':
        if len(sys.argv) < 3:
            print("Usage: python utils.py toggle <domain>")
            return
        toggle_mapping_cli(sys.argv[2])
    
    elif command == 'stats':
        if len(sys.argv) < 3:
            print("Usage: python utils.py stats <domain>")
            return
        show_stats(sys.argv[2])
    
    elif command == 'export':
        filename = sys.argv[2] if len(sys.argv) > 2 else 'mappings_export.csv'
        export_mappings(filename)
    
    elif command == 'backup':
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        backup_database(filename)
    
    elif command == 'reset-clicks':
        domain = sys.argv[2] if len(sys.argv) > 2 else None
        reset_clicks(domain)
    
    else:
        print(f"Unknown command: {command}")
        print("Run 'python utils.py' for help")

if __name__ == '__main__':
    main()
