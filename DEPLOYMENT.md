# 🚀 MaskDNS Deployment Guide

Complete step-by-step deployment instructions for free hosting platforms.

## 📋 Pre-Deployment Checklist

- [ ] Application tested locally
- [ ] Strong admin password chosen
- [ ] Domain ready (or using free subdomain)
- [ ] Hosting platform account created

---

## 1️⃣ PythonAnywhere Deployment (RECOMMENDED)

**Cost**: FREE (up to 1 web app)
**Difficulty**: Easy
**Setup Time**: 10 minutes

### Step-by-Step:

#### A. Create Account
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Click "Pricing & signup"
3. Choose "Create a Beginner account" (FREE)
4. Verify email and login

#### B. Upload Code

**Option 1: Git Clone (Recommended)**
1. Go to "Consoles" tab
2. Click "Bash"
3. Run:
```bash
git clone https://github.com/yourusername/maskdns.git
cd maskdns
```

**Option 2: Manual Upload**
1. Go to "Files" tab
2. Click "Upload a file"
3. Upload all project files
4. Create folders: `templates/`, `static/`

#### C. Install Dependencies
In Bash console:
```bash
cd maskdns
pip3 install --user -r requirements.txt
```

#### D. Initialize Database
```bash
python3 -c "from app import init_db; init_db()"
```

#### E. Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10
5. Click through setup

#### F. Edit WSGI Configuration
1. In Web tab, click WSGI configuration file link
2. Delete all content
3. Paste:
```python
import sys
import os

# Add your project directory
path = '/home/YOURUSERNAME/maskdns'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['ADMIN_PASSWORD'] = 'your-secure-password-here'
os.environ['SECRET_KEY'] = 'your-secret-key-here'
os.environ['DEBUG'] = 'False'

from app import app as application
```
4. Replace `YOURUSERNAME` with your PythonAnywhere username
5. Replace passwords with secure values
6. Click Save

#### G. Configure Static Files
1. In Web tab, scroll to "Static files"
2. Add:
   - URL: `/static/`
   - Directory: `/home/YOURUSERNAME/maskdns/static/`

#### H. Reload and Test
1. Click green "Reload" button
2. Visit: `https://yourusername.pythonanywhere.com`
3. Should see MaskDNS landing page!

#### I. Setup Custom Domain (Optional)
1. In Web tab, add your domain
2. Point domain DNS to PythonAnywhere IP (shown in Web tab)
3. Wait for DNS propagation (30 minutes)

### Troubleshooting PythonAnywhere:
- **500 Error**: Check error log in Web tab
- **Import errors**: Verify all dependencies installed
- **Path issues**: Double-check paths in WSGI file
- **Database error**: Re-run init_db command

---

## 2️⃣ Render Deployment

**Cost**: FREE (with limitations)
**Difficulty**: Medium
**Setup Time**: 5 minutes

### Step-by-Step:

#### A. Prepare Repository
1. Push code to GitHub/GitLab
2. Make sure `render.yaml` is in root
3. Commit all files

#### B. Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Verify email

#### C. Create Web Service
1. Click "New +"
2. Select "Web Service"
3. Connect your repository
4. Or use "Deploy from public Git repository"

#### D. Configure Service
- **Name**: `maskdns`
- **Environment**: `Python 3`
- **Region**: Choose closest
- **Branch**: `main` or `master`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

#### E. Add Environment Variables
1. Scroll to "Environment Variables"
2. Add:
```
ADMIN_PASSWORD = your-secure-password
SECRET_KEY = generate-random-string-here
DEBUG = False
```

#### F. Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for first deploy
3. Your app will be at: `https://maskdns.onrender.com`

#### G. Initialize Database
1. Go to Shell tab in Render dashboard
2. Run:
```bash
python -c "from app import init_db; init_db()"
```

### Render Limitations (Free Tier):
- ⚠️ Sleeps after 15 minutes of inactivity
- ⚠️ 750 hours/month free
- ⚠️ Slower cold starts

### Custom Domain on Render:
1. Go to Settings → Custom Domain
2. Add your domain
3. Configure DNS per Render instructions

---

## 3️⃣ Fly.io Deployment

**Cost**: FREE (generous limits)
**Difficulty**: Advanced
**Setup Time**: 10 minutes

### Step-by-Step:

#### A. Install Fly CLI

**macOS**:
```bash
brew install flyctl
```

**Linux/WSL**:
```bash
curl -L https://fly.io/install.sh | sh
```

**Windows**:
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

#### B. Sign Up & Login
```bash
fly auth signup  # or fly auth login
```

#### C. Launch App
```bash
cd maskdns
fly launch
```

Follow prompts:
- App name: `maskdns` (or unique name)
- Region: Choose closest
- PostgreSQL: No
- Redis: No
- Deploy: No (we'll set secrets first)

#### D. Set Secrets
```bash
fly secrets set ADMIN_PASSWORD=your-secure-password
fly secrets set SECRET_KEY=your-secret-key
fly secrets set DEBUG=False
```

#### E. Deploy
```bash
fly deploy
```

#### F. Initialize Database
```bash
fly ssh console
python -c "from app import init_db; init_db()"
exit
```

#### G. Access App
```bash
fly open
```

### Fly.io Custom Domain:
```bash
fly certs add yourdomain.com
```
Then add DNS records as shown.

---

## 🌐 DNS Configuration Guide

### For ANY Hosting Platform:

#### Step 1: Get Server IP

**PythonAnywhere**:
```bash
ping yourusername.pythonanywhere.com
```

**Render**:
Look in dashboard or:
```bash
nslookup maskdns.onrender.com
```

**Fly.io**:
```bash
fly ips list
```

#### Step 2: Add DNS Records

Login to your domain registrar (Namecheap, GoDaddy, Cloudflare, etc.):

**For subdomain** (e.g., `app.yourdomain.com`):
```
Type: A
Name: app
Value: YOUR_SERVER_IP
TTL: 300
```

**For root domain** (e.g., `yourdomain.com`):
```
Type: A
Name: @
Value: YOUR_SERVER_IP
TTL: 300
```

#### Step 3: Wait for DNS Propagation
- Usually 5-30 minutes
- Can take up to 48 hours in rare cases
- Check progress: `nslookup yourdomain.com`

#### Step 4: Test
```bash
curl -I http://yourdomain.com
```

---

## 🆓 Free Domain Services

### Option A: DuckDNS (Subdomain)
1. Visit [duckdns.org](https://www.duckdns.org)
2. Login with Google/GitHub
3. Create subdomain: `yourapp`
4. You get: `yourapp.duckdns.org`
5. Point to your server IP
6. Update every 5 minutes (use cron)

### Option B: Freenom (Full Domain)
1. Visit [freenom.com](https://www.freenom.com)
2. Search for domain
3. Available TLDs: `.tk`, `.ml`, `.ga`, `.cf`, `.gq`
4. Free for 12 months
5. Manage DNS in dashboard

**⚠️ Note**: Freenom domains may be reclaimed if inactive

### Option C: Cloudflare Pages (Domain + Hosting)
1. Sign up at [cloudflare.com](https://www.cloudflare.com)
2. Add your domain or register new one
3. Use Cloudflare nameservers
4. Free SSL included!

---

## 🔒 SSL/HTTPS Setup

### PythonAnywhere
- ✅ Automatic HTTPS on `.pythonanywhere.com`
- ❌ Custom domains need paid plan for HTTPS

### Render
- ✅ Automatic HTTPS for all domains
- ✅ Auto-renewing certificates

### Fly.io
- ✅ Automatic HTTPS
- ✅ Certificate management built-in

### Free SSL with Cloudflare:
1. Add domain to Cloudflare
2. Update nameservers at registrar
3. Enable "SSL/TLS" → "Full"
4. Enable "Always Use HTTPS"
5. Done! Free SSL for life.

---

## 📊 Post-Deployment Testing

### Test Checklist:

1. **Landing Page**:
```bash
curl https://your-app-url.com
```

2. **Admin Login**:
Visit: `https://your-app-url.com/admin/login`
Enter your password

3. **Add Test Mapping**:
- Domain: `test.yourdomain.com`
- Target: `https://example.com`

4. **Configure DNS**:
Point `test.yourdomain.com` to server IP

5. **Wait & Test**:
After DNS propagates, visit `test.yourdomain.com`

6. **Check Stats**:
Visit: `https://your-app-url.com/stats/test.yourdomain.com`

---

## 🐛 Common Issues & Fixes

### Issue: "Module not found"
**Fix**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Database is locked"
**Fix**: Check file permissions
```bash
chmod 666 domains.db
```

### Issue: "502 Bad Gateway"
**Fix**: 
- Check target URL is accessible
- Increase timeout in environment variables
- Check hosting platform logs

### Issue: "Admin password not working"
**Fix**:
- Verify environment variable is set
- Restart application
- Check for typos in password

### Issue: "Domain not proxying"
**Fix**:
- Verify DNS points to correct IP
- Check mapping is active in admin panel
- Ensure domain spelling matches exactly

---

## 📈 Monitoring & Maintenance

### Check Application Health:
```bash
curl -I https://your-app-url.com
```

### View Logs:

**PythonAnywhere**: Web tab → Log files
**Render**: Logs tab in dashboard
**Fly.io**: `fly logs`

### Database Backup:

**PythonAnywhere**:
```bash
cp domains.db domains.db.backup
```

**Render/Fly.io**:
Download via dashboard or CLI

### Update Application:

**PythonAnywhere**:
```bash
cd maskdns
git pull
# Reload in Web tab
```

**Render**: Auto-deploys on git push

**Fly.io**:
```bash
fly deploy
```

---

## 💡 Pro Tips

1. **Use Cloudflare** for free SSL and DDoS protection
2. **Set strong password** via environment variables
3. **Monitor uptime** with UptimeRobot (free)
4. **Backup database** regularly
5. **Use logging** for debugging issues
6. **Rate limit** using Cloudflare
7. **Cache responses** for better performance
8. **Set up alerts** for downtime

---

## 🎉 Success!

Your MaskDNS application should now be live and masking domains!

**Next Steps**:
1. Add your first domain mapping
2. Share your custom domains
3. Monitor analytics
4. Enjoy your branded URLs!

**Need Help?**
- Check main README.md
- Review application logs
- Open an issue on GitHub

---

**Made with ❤️ for developers who love free tools!**
