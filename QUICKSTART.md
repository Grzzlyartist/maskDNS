# ⚡ MaskDNS Quick Start Guide

Get MaskDNS running in 5 minutes!

## 🚀 Super Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open browser
# Landing: http://localhost:5000
# Admin: http://localhost:5000/admin/login
# Password: admin123
```

That's it! 🎉

---

## 📝 First Domain Mapping (Example)

### Scenario:
You have a Vercel app at `my-portfolio.vercel.app` and want it to appear at `portfolio.mybrand.com`

### Steps:

#### 1. Setup DNS
In your domain registrar (GoDaddy, Namecheap, etc.):
```
Type: A
Name: portfolio
Value: YOUR_SERVER_IP (from hosting provider)
TTL: 300
```

#### 2. Add Mapping
1. Go to `http://localhost:5000/admin/login`
2. Login with password: `admin123`
3. Fill in form:
   - **Custom Domain**: `portfolio.mybrand.com`
   - **Target URL**: `https://my-portfolio.vercel.app`
4. Click "Add Mapping"

#### 3. Wait for DNS (5-30 minutes)
Check if DNS is ready:
```bash
nslookup portfolio.mybrand.com
```

#### 4. Test!
Visit `http://portfolio.mybrand.com`
- You should see your Vercel app
- URL bar shows `portfolio.mybrand.com`
- Success! ✅

---

## 🎯 Real Use Cases

### Case 1: Hide Vercel Domain
```
Before: https://my-nextjs-app-abc123.vercel.app
After:  https://app.mybusiness.com
```

### Case 2: Professional Portfolio
```
Before: https://john-doe-portfolio.netlify.app  
After:  https://johndoe.com
```

### Case 3: Staging Environment
```
Before: https://staging-app-xyz.herokuapp.com
After:  https://staging.myapp.com
```

### Case 4: Client Demo
```
Before: https://client-demo-v2.render.app
After:  https://demo.clientname.com
```

---

## 🆓 Free Everything Setup

### 1. Free Hosting → PythonAnywhere
- Sign up: [pythonanywhere.com](https://www.pythonanywhere.com)
- Deploy: See DEPLOYMENT.md
- Cost: $0/month

### 2. Free Domain → Freenom
- Sign up: [freenom.com](https://www.freenom.com)
- Get: `.tk`, `.ml`, `.ga`, `.cf`, `.gq`
- Cost: $0/year

### 3. Free SSL → Cloudflare
- Sign up: [cloudflare.com](https://www.cloudflare.com)
- Add domain, enable SSL
- Cost: $0/forever

**Total Cost: $0** 💰

---

## 🔒 Security Checklist

Before going live:

- [ ] Change admin password from default
- [ ] Set strong `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Set `DEBUG=False`
- [ ] Backup database regularly
- [ ] Monitor access logs

---

## 🐛 Quick Troubleshooting

### Problem: Can't login to admin
**Solution**: Default password is `admin123`

### Problem: Domain shows "Not Configured"
**Solution**: 
1. Check DNS is pointing to server
2. Verify mapping exists in admin panel
3. Ensure mapping is active

### Problem: Shows target domain in URL
**Solution**: Check that you're using the correct custom domain

### Problem: 502 Error
**Solution**:
1. Check target URL is accessible
2. Verify target URL is correct
3. Check app logs for errors

---

## 📚 Learn More

- **Full Guide**: See README.md
- **Deployment**: See DEPLOYMENT.md  
- **Database**: SQLite file `domains.db`
- **Logs**: Check hosting platform logs

---

## 🎓 Example Workflow

```bash
# Local Development
pip install -r requirements.txt
python app.py
# Visit http://localhost:5000

# Add Test Mapping
# Domain: test.example.com
# Target: https://example.com

# Deploy to PythonAnywhere
git push
# Or upload files manually

# Configure DNS
# test.example.com → A → SERVER_IP

# Wait 15 minutes for DNS

# Visit your domain
# http://test.example.com
# Should show example.com content!
```

---

## ✨ Pro Tips

1. **Test with localhost first**: Use `127.0.0.1` in `/etc/hosts` for testing
2. **Use subdomains**: Easier than root domains
3. **Cloudflare caching**: Speed up responses
4. **Monitor uptime**: Use UptimeRobot (free)
5. **Backup often**: `cp domains.db backup/`

---

## 🎉 That's It!

You now have a complete domain masking service running for free!

**Questions?** Check README.md or open an issue.

**Working?** Star the repo and share with friends! ⭐

---

**Happy Masking! 🎭**
