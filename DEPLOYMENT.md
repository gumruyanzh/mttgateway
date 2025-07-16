# 🚀 MTT Gateway - Free Deployment Guide

## Quick Deployment Options

### 🛤️ **Railway** (Recommended)

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub**: Link your `mttgateway` repository
3. **Deploy**: Railway auto-detects Django and deploys
4. **Database**: Railway provides free PostgreSQL
5. **Environment Variables**: Set in Railway dashboard:
   ```
   DJANGO_SETTINGS_MODULE=mtt_gateway.settings_production
   SECRET_KEY=your-super-secret-key-here
   ```

**Deployment URL**: `https://your-app-name.railway.app`

---

### 🎨 **Render**

1. **Sign up** at [render.com](https://render.com)
2. **New Web Service**: Connect your GitHub repo
3. **Settings**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn mtt_gateway.wsgi:application`
4. **Environment Variables**:
   ```
   DJANGO_SETTINGS_MODULE=mtt_gateway.settings_production
   SECRET_KEY=your-super-secret-key-here
   ```

**Free Database**: Create separate PostgreSQL service (free for 90 days)

---

### 🐍 **PythonAnywhere**

1. **Sign up** at [pythonanywhere.com](https://pythonanywhere.com)
2. **Upload Code**: Use Git or file upload
3. **Web App Setup**:
   - Choose Django
   - Python 3.9+
   - Point to `mtt_gateway/wsgi.py`
4. **Database**: Use included MySQL database

---

### 🚁 **Heroku** (Paid - $5/month minimum)

1. **Install Heroku CLI**
2. **Commands**:
   ```bash
   heroku create your-app-name
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

---

## 📋 **Pre-Deployment Checklist**

### ✅ **Files Already Created**
- ✅ `Procfile` - Process definitions
- ✅ `railway.toml` - Railway configuration  
- ✅ `requirements.txt` - Dependencies
- ✅ `settings_production.py` - Production settings

### 🔧 **Environment Variables to Set**
```env
DJANGO_SETTINGS_MODULE=mtt_gateway.settings_production
SECRET_KEY=your-super-secret-key-generate-new-one
DEBUG=False
```

### 📊 **Database Migration**
Most platforms auto-run migrations, but if needed:
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## 🌐 **Access Your Deployed App**

### **Main URLs**
- **Homepage**: `https://your-app.platform.com/`
- **Admin Panel**: `https://your-app.platform.com/admin/`
- **API Endpoints**: `https://your-app.platform.com/api/`

### **API Examples**
- Tokens: `https://your-app.platform.com/api/tokens/`
- Wallets: `https://your-app.platform.com/api/wallets/`
- Customers: `https://your-app.platform.com/api/customers/`
- Merchants: `https://your-app.platform.com/api/merchant/`

---

## 🆓 **Platform Comparison**

| Platform | Free Tier | Database | Custom Domain | Best For |
|----------|-----------|----------|---------------|----------|
| **Railway** | 500h/month | PostgreSQL ✅ | ✅ | Development |
| **Render** | 750h/month | PostgreSQL (90 days) | ✅ | Production |
| **PythonAnywhere** | Always on | MySQL ✅ | ❌ (paid) | Django focus |
| **Heroku** | $5/month | PostgreSQL ✅ | ✅ | Enterprise |

---

## 🚨 **Important Notes**

1. **Generate New SECRET_KEY**: Never use the default in production
2. **Database**: SQLite works for testing, PostgreSQL for production
3. **Static Files**: Whitenoise handles CSS/JS serving
4. **Security**: Production settings include security headers
5. **Monitoring**: Check platform logs for any deployment issues

---

## 📞 **Need Help?**

- Check platform documentation
- Review Django deployment guides
- Monitor application logs
- Test API endpoints after deployment 