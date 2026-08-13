# ❓ MaskDNS Frequently Asked Questions

## General Questions

### What is MaskDNS?
MaskDNS is a free, self-hosted domain masking service that allows you to hide free subdomains (like Vercel, Netlify, Heroku) behind your own custom domains. The browser URL bar shows your custom domain while proxying content from the target URL.

### Is it really free?
Yes! The application is open-source and can be deployed on free hosting platforms like PythonAnywhere, Render, or Fly.io. There are no paid features or hidden costs.

### How does it work?
MaskDNS acts as a reverse proxy. When someone visits your custom domain, the server fetches content from your target URL and serves it, keeping your custom domain in the browser's address bar.

### Is it legal?
Yes, as long as you own both the custom domain and have rights to proxy the target content. Don't use it to impersonate or steal content from others.

---

## Setup Questions

### Do I need a domain?
Not necessarily! You can use free subdomain services like DuckDNS or register free domains from Freenom. See the DEPLOYMENT.md guide for details.

### Can I use a subdomain?
Yes! Subdomains work perfectly. For example: `app.mybrand.com` or `demo.mysite.com`

### How long does DNS take to propagate?
Usually 5-30 minutes, but can take up to 48 hours in rare cases. You can check progress with:
```bash
nslookup your-domain.com
```

### What if I don't have a server?
Deploy MaskDNS to free hosting platforms:
- **PythonAnywhere** (recommended for beginners)
- **Render** (auto-deploys from git)
- **Fly.io** (more advanced)

See DEPLOYMENT.md for step-by-step guides.

---

## Technical Questions

### What happens to query parameters?
Query parameters are preserved and forwarded to the target URL. For example:
```
Custom: app.example.com?page=2&sort=name
Target: myapp.vercel.app?page=2&sort=name
```

### Are paths preserved?
Yes! All paths are maintained:
```
Custom: app.example.com/products/123
Target: myapp.vercel.app/products/123
```

### Does it work with POST requests?
Yes, all HTTP methods (GET, POST, PUT, DELETE, etc.) are supported.

### Can I mask multiple domains?
Absolutely! Add as many domain mappings as you need. There's no limit.

### Does it support HTTPS/SSL?
Yes, but you need to:
1. Deploy to a platform with SSL support (Render, Fly.io)
2. Or use Cloudflare for free SSL
3. PythonAnywhere requires paid plan for custom domain SSL

### What about cookies and sessions?
Cookies are forwarded between the custom domain and target URL. Sessions should work normally.

---

## Performance Questions

### Is there a speed penalty?
Yes, there's a small latency overhead since requests go through the proxy server. Typically 50-200ms depending on server location and target URL.

### Can I cache responses?
The current version doesn't cache, but you can:
1. Use Cloudflare caching
2. Add Redis caching (requires code modification)
3. Use a CDN

### What's the timeout limit?
Default is 30 seconds. You can change it via the `TIMEOUT` environment variable.

### Will it handle high traffic?
Free tier hosting has limitations:
- **PythonAnywhere**: 100k hits/day
- **Render**: 750 hours/month (sleeps when inactive)
- **Fly.io**: 160GB bandwidth/month

For high traffic, consider paid hosting or Cloudflare caching.

---

## Troubleshooting

### "Domain Not Configured" error?
This means:
1. DNS hasn't propagated yet (wait longer)
2. Domain mapping doesn't exist (add in admin panel)
3. Domain is deactivated (toggle in admin)
4. Domain spelling mismatch (check carefully)

### "502 Bad Gateway" error?
Possible causes:
1. Target URL is down or inaccessible
2. Request timeout (increase `TIMEOUT`)
3. Target URL blocks proxy requests
4. Network connectivity issues

### Admin password not working?
1. Check you're using the correct password
2. Verify `ADMIN_PASSWORD` environment variable is set
3. Restart the application after changing env vars
4. Clear browser cache and cookies

### Target URL shows in browser?
This shouldn't happen with proper setup. Check:
1. DNS points to your MaskDNS server (not target)
2. Mapping exists and is active
3. No browser extensions interfering
4. Target URL isn't doing client-side redirects

### Forms don't submit?
Forms should work if:
1. Method is POST/GET (supported)
2. Action URL is relative (not absolute to target)
3. No CORS issues on target

If problems persist, the target site might have anti-proxy measures.

---

## Security Questions

### Is it secure?
Basic security is implemented:
- Password-protected admin panel
- Input validation and sanitization
- SQL injection prevention (parameterized queries)
- Session management

For production:
- Use strong passwords
- Enable HTTPS
- Use Cloudflare for DDoS protection
- Monitor logs regularly

### Can others see my target URL?
The target URL is:
- Visible in admin panel (password-protected)
- Stored in database
- NOT visible to end users
- NOT in page source (unless target reveals it)

### Should I backup the database?
Yes! Regular backups are recommended:
```bash
cp domains.db domains.db.backup
```

Or use the utility:
```bash
python utils.py backup
```

### Can someone abuse my proxy?
Potential risks:
- Someone could add mappings if they get admin password
- High traffic could exhaust resources
- Hosting provider might suspend for violations

Mitigations:
- Use strong admin password
- Monitor access logs
- Use rate limiting (Cloudflare)
- Review mappings regularly

---

## Feature Questions

### Can I customize the error pages?
Yes! Edit the templates:
- `templates/error.html` - General errors
- `templates/not_configured.html` - Domain not found

### Can I white-label the interface?
Absolutely! Customize:
- `templates/` - All HTML pages
- `static/style.css` - Styling
- Change branding, colors, logos

### Can I add user accounts?
Not in the current version. It's designed for single admin use. You could fork and add multi-user support.

### Can I track more analytics?
Current tracking:
- Click counts per domain
- Created date

To add more:
1. Modify database schema
2. Update tracking code in `app.py`
3. Add to admin dashboard

### Can I add API access?
Not currently, but you could add API endpoints with authentication for programmatic access to mappings.

---

## Comparison Questions

### vs Cloudflare Workers?
**MaskDNS Pros**:
- Easier setup
- Visual admin panel
- No coding required

**Cloudflare Workers Pros**:
- Better performance
- More scalable
- Edge computing

### vs nginx reverse proxy?
**MaskDNS Pros**:
- Web-based management
- No server configuration needed
- Easier for non-technical users

**nginx Pros**:
- Better performance
- More configuration options
- Production-grade

### vs URL shorteners?
**MaskDNS Advantages**:
- Full domain masking (not just homepage)
- Preserves all paths and parameters
- Professional branding
- No redirect (stays on your domain)

---

## Cost Questions

### What does it cost to run?
**100% Free Option**:
- Hosting: PythonAnywhere free tier
- Domain: Freenom free domain
- SSL: Cloudflare free SSL
- **Total: $0/month**

**Professional Option**:
- Hosting: PythonAnywhere ($5/month) or VPS ($5-10/month)
- Domain: .com domain ($10-15/year)
- SSL: Let's Encrypt (free) or Cloudflare (free)
- **Total: ~$7-12/month**

### Are there hidden costs?
No! The application itself is free and open-source. Costs only come from:
- Hosting (can be free)
- Domain registration (can be free)
- SSL certificates (can be free)

---

## Upgrade Questions

### How do I update MaskDNS?
**PythonAnywhere**:
```bash
cd maskdns
git pull origin main
# Reload in Web tab
```

**Render**: Auto-deploys on git push

**Fly.io**:
```bash
fly deploy
```

### Will updates break my data?
Database schema changes are rare. Always backup before updating:
```bash
python utils.py backup
```

### Can I migrate to a bigger server?
Yes! Just:
1. Export your database
2. Install on new server
3. Import database
4. Update DNS to new IP

---

## Advanced Questions

### Can I modify the code?
Yes! It's open-source. Common modifications:
- Add custom authentication
- Implement caching
- Add more analytics
- Custom error handling
- Rate limiting

### Can I use with Docker?
Yes! Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
```

### Can I use PostgreSQL instead of SQLite?
Yes, but requires code changes:
1. Replace SQLite with PostgreSQL adapter
2. Update connection strings
3. Modify queries if needed

### Can I run multiple instances?
Yes, for load balancing. But you'll need:
1. Shared database (PostgreSQL/MySQL)
2. Load balancer
3. Session storage (Redis)

---

## Support Questions

### Where do I get help?
1. Check this FAQ
2. Read README.md and DEPLOYMENT.md
3. Review application logs
4. Open issue on GitHub
5. Check existing GitHub issues

### How do I report bugs?
Open an issue on GitHub with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Application logs
- Environment details

### Can I request features?
Yes! Open a feature request on GitHub. Popular requests may be implemented.

---

## License & Usage

### What license is it under?
MIT License - you can use it for any purpose, including commercial projects.

### Can I use it for my business?
Yes! The MIT license allows commercial use.

### Do I need to credit MaskDNS?
Not required by the license, but appreciated!

### Can I sell it?
Yes, you can offer it as a service or sell customized versions.

---

**Still have questions?** Open an issue on GitHub or check the documentation!
