# SAI Fitness Backend - Render Deployment Guide

## 🚀 Deploy to Render (Fastest & Easiest)

Render is perfect for Django apps with automatic deployments, free PostgreSQL, and zero configuration needed!

## 🎯 **Why Render?**
- ✅ **Free tier** with 750 hours/month
- ✅ **Automatic deployments** from GitHub
- ✅ **Free PostgreSQL** database (1GB)
- ✅ **SSL certificates** included
- ✅ **No credit card** required for free tier
- ✅ **Zero configuration** - just connect GitHub!

## 📋 Prerequisites
- ✅ GitHub Repository (already done!)
- ✅ Render Account (sign up at [render.com](https://render.com))
- ✅ Cloudinary Account (for media storage)

## 🚀 **Quick Deployment (3 minutes)**

### Step 1: Create Render Account
1. Go to **[render.com](https://render.com)**
2. **Sign up with GitHub** (easiest option)
3. Authorize Render to access your repositories

### Step 2: Deploy Web Service
1. **Click "New +" → "Web Service"**
2. **Connect Repository:**
   ```
   Repository: Adi-Yadav1/Aarohan_Backend
   Branch: main
   ```
3. **Configure Service:**
   ```
   Name: sai-fitness-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn Aaarohan_Backend.wsgi:application
   ```
4. **Click "Create Web Service"** 🎉

### Step 3: Add PostgreSQL Database
1. **Click "New +" → "PostgreSQL"**
2. **Configure:**
   ```
   Name: sai-fitness-db
   Database: sai_fitness
   User: sai_user
   Region: Same as web service
   Plan: Free ($0/month)
   ```
3. **Click "Create Database"**

### Step 4: Configure Environment Variables
**In your Web Service → Environment:**

```env
# Django Settings
SECRET_KEY=your-super-secret-random-key-here
DEBUG=False
ALLOWED_HOSTS=sai-fitness-backend.onrender.com

# Database (Render provides this automatically)
DATABASE_URL=postgresql://sai_user:password@hostname:5432/sai_fitness

# Cloudinary Settings
CLOUDINARY_CLOUD_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Email Settings (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password

# Python Path
PYTHON_VERSION=3.11.0
```

### Step 5: Database Setup
**Render automatically runs migrations, but if needed:**

1. **Go to Web Service → Shell**
2. **Run commands:**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser  # Optional
```

## 🌐 **Your Live API**

After deployment (takes 2-3 minutes):
```
Base URL: https://sai-fitness-backend.onrender.com/api/

Test your API:
curl https://sai-fitness-backend.onrender.com/api/tests/
```

## 📱 **All 19+ API Endpoints Available:**

```
Authentication:
POST /api/auth/register/     - User registration
POST /api/auth/login/        - User login
POST /api/auth/logout/       - User logout
POST /api/auth/token/refresh/ - Refresh JWT

Athletes & Profiles:
GET  /api/athletes/profile/   - Get user profile
PUT  /api/athletes/profile/   - Update profile
POST /api/athletes/register/  - Register athlete
GET  /api/athletes/          - List athletes

Performance & Tests:
GET  /api/tests/             - Available tests
POST /api/performance/submit/ - Submit performance
GET  /api/performance/history/ - Performance history
GET  /api/performance/analytics/ - Analytics

Leaderboards:
GET  /api/leaderboard/       - Global leaderboard
GET  /api/leaderboard/events/<id>/ - Event leaderboard

Badges & Notifications:
GET  /api/badges/            - Available badges
GET  /api/badges/my-badges/  - User badges
GET  /api/notifications/     - User notifications
PUT  /api/notifications/<id>/read/ - Mark as read
```

## 💰 **Render Pricing**

### **Free Tier (Perfect for development):**
- ✅ Web Service: 750 hours/month (enough for 24/7)
- ✅ PostgreSQL: 1GB storage, 97 connections
- ✅ Custom domains supported
- ✅ Automatic SSL certificates
- ✅ No credit card required

### **Paid Plans (Production):**
- **Starter**: $7/month (always-on, no sleep)
- **Standard**: $25/month (faster builds, more resources)

## 🔧 **Auto-Deploy Features**

Render automatically:
- ✅ Installs packages from `requirements.txt`
- ✅ Runs database migrations
- ✅ Collects static files
- ✅ Starts your app with `gunicorn`
- ✅ Provides HTTPS certificates
- ✅ Redeploys on every GitHub push

## ⚡ **Alternative: One-Click Deploy**

Create this button in your GitHub README:
```markdown
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Adi-Yadav1/Aarohan_Backend)
```

## 🐛 **Common Issues & Solutions**

### Build Fails?
```bash
# Check your requirements.txt has all packages
# Render automatically detects Python version from runtime.txt
```

### Database Connection Issues?
```bash
# Render provides DATABASE_URL automatically
# Make sure your settings.py uses dj_database_url
```

### Static Files Not Loading?
```bash
# Render runs collectstatic automatically
# Check STATIC_URL and STATICFILES_DIRS in settings.py
```

## 🎯 **Quick Commands for Render Shell**

```bash
# Check Django version
python --version
django-admin --version

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Check database connection
python manage.py dbshell

# Load sample data (if you created fixtures)
python manage.py loaddata sample_data.json
```

## 🎉 **Deployment Complete!**

Your SAI Fitness backend will be live with:
- ✅ **19+ REST API endpoints**
- ✅ **JWT Authentication**
- ✅ **PostgreSQL Database**  
- ✅ **File Upload (Cloudinary)**
- ✅ **Email Notifications**
- ✅ **Admin Interface**
- ✅ **Automatic HTTPS**
- ✅ **Auto-deployments**

**Your React Native app can now connect to:**
```
https://sai-fitness-backend.onrender.com/api/
```

## 🚀 **Next Steps After Deployment**

1. **Test all endpoints** using Postman or curl
2. **Create sample data** through admin or API
3. **Configure CORS** for your React Native app
4. **Set up monitoring** (Render provides basic logs)
5. **Update frontend** to use production API URL

Render makes deployment incredibly simple - just connect GitHub and you're live! 🎉