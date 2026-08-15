# MaskDNS

A Flask-based reverse proxy that masks URLs behind custom domains or path-based shortcuts. Built with Flask and SQLite.

## How It Works

MaskDNS supports two modes:

**DNS-based masking** — Point a custom domain at your server via an A record. Incoming requests are matched by `Host` header and proxied to the configured target URL. Visitors see your custom domain throughout.

**Path-based masking** — No DNS required. Access via `/m/<masked-id>` and traffic is proxied to the mapped target. Good for quick sharing or testing.

In both cases, content is fetched server-side and returned transparently, with click tracking on every request.

## Features

- Two proxy modes: DNS-based and path-based (`/m/<id>`)
- Password-protected admin panel (add, delete, toggle mappings)
- Per-domain click tracking with a stats page
- SQLite storage — zero external dependencies
- CLI tools for DB management via `utils.py`

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

- Landing page: `http://localhost:5000`
- Admin panel: `http://localhost:5000/admin/login`
- Default password: `admin123`

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `ADMIN_PASSWORD` | `admin123` | Admin panel password |
| `SECRET_KEY` | `dev-secret-key-...` | Flask session secret |
| `DATABASE_PATH` | `domains.db` | Path to SQLite database |
| `TIMEOUT` | `30` | Proxy request timeout (seconds) |
| `DEBUG` | `False` | Flask debug mode |

Copy `.env.example` to `.env` and fill in values before deploying.

## DNS Setup (for DNS-based mode)

Add an A record in your domain's DNS settings:

```
Type:  A
Name:  app        (or @ for root)
Value: YOUR_SERVER_IP
TTL:   300
```

Finding your server IP:
- Render: listed in the service dashboard
- Fly.io: `fly ips list`
- PythonAnywhere: `ping yourusername.pythonanywhere.com`

DNS propagation typically takes 5–30 minutes. Check with `nslookup app.yourdomain.com`.

Then add the mapping in the admin panel: set custom domain to `app.yourdomain.com` and target URL to your app.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for full guides on Render, Fly.io, and PythonAnywhere.

### Render (quick)

```
Build command:  pip install -r requirements.txt
Start command:  gunicorn app:app
Env vars:       ADMIN_PASSWORD, SECRET_KEY
```

### Fly.io (quick)

```bash
fly launch
fly secrets set ADMIN_PASSWORD=your-password SECRET_KEY=your-secret
fly deploy
```

## CLI Tools

`utils.py` provides command-line access to the database:

```bash
python utils.py list
python utils.py add app.example.com https://myapp.vercel.app
python utils.py delete app.example.com
python utils.py toggle app.example.com
python utils.py stats app.example.com
python utils.py export [filename]
python utils.py backup [filename]
python utils.py reset-clicks [domain]
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Landing page |
| GET/POST | `/admin/login` | Admin login |
| GET | `/admin` | Admin panel |
| POST | `/admin/add` | Add mapping |
| POST | `/admin/delete/<id>` | Delete mapping |
| POST | `/admin/toggle/<id>` | Toggle active status |
| GET | `/stats/<domain>` | Domain stats |
| GET | `/m/<masked-id>` | Path-based proxy |
| GET | `/<path>` | DNS-based proxy |

## Database Schema

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

## Troubleshooting

**Domain shows "not configured"** — Check the admin panel, verify the domain matches exactly (no `http://`, no trailing slash), and that the mapping is active.

**502 Bad Gateway** — Target URL is unreachable or blocking proxy requests. Try opening the target URL directly, or increase `TIMEOUT`.

**DNS not resolving** — Propagation can take up to 48h. Check with `nslookup` or [dnschecker.org](https://dnschecker.org).

**Admin password rejected** — Confirm `ADMIN_PASSWORD` env var is set and the app has been restarted since the change.

## License

MIT
