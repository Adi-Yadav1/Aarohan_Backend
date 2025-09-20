# SAI Fitness Backend - Azure App Service Deployment Guide

## 🚀 Deploy SAI Fitness Backend to Azure

Azure App Service provides excellent Django hosting with integrated PostgreSQL, auto-scaling, and CI/CD from GitHub.

## 📋 Prerequisites

1. **Azure Account** - Sign up at [portal.azure.com](https://portal.azure.com)
2. **GitHub Repository** - Your code is already pushed to GitHub ✅
3. **Cloudinary Account** - For media storage [cloudinary.com](https://cloudinary.com)

## 🎯 Step-by-Step Azure Deployment

### Step 1: Create Azure App Service

1. **Log into [Azure Portal](https://portal.azure.com)**
2. **Click "Create a resource"**
3. **Search for "Web App" → Click "Create"**
4. **Configure Basic Settings:**
   ```
   Resource Group: Create new "SAI-Fitness-RG"
   Name: sai-fitness-backend (must be globally unique)
   Runtime Stack: Python 3.11
   Operating System: Linux
   Region: East US (or your preferred region)
   Pricing: B1 Basic ($7.30/month) or F1 Free
   ```

### Step 2: Configure GitHub Deployment

1. **In App Service → Deployment Center**
2. **Select "GitHub" as source**
3. **Authorize Azure with your GitHub account**
4. **Select:**
   ```
   Organization: Your GitHub username
   Repository: Aarohan_Backend
   Branch: main
   ```
5. **Build Provider: GitHub Actions**
6. **Click "Save"** - Azure will create deployment workflow

### Step 3: Create PostgreSQL Database

1. **Create new resource → "Azure Database for PostgreSQL"**
2. **Select "Flexible Server"**
3. **Configure:**
   ```
   Resource Group: SAI-Fitness-RG
   Server name: sai-fitness-db (globally unique)
   Region: Same as App Service
   PostgreSQL Version: 15
   Compute + Storage: Burstable B1ms ($7.10/month)
   Admin username: saiadmin
   Password: Create strong password
   ```

### Step 4: Configure App Service Settings

**In Azure Portal → Your App Service → Configuration → Application Settings:**

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here-random-50-chars
DEBUG=False
ALLOWED_HOSTS=sai-fitness-backend.azurewebsites.net

# Database (from PostgreSQL resource)
DATABASE_URL=postgresql://saiadmin:password@sai-fitness-db.postgres.database.azure.com:5432/postgres?sslmode=require

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

# Azure-specific
SCM_DO_BUILD_DURING_DEPLOYMENT=true
WEBSITE_HTTPLOGGING_RETENTION_DAYS=7
```

### Step 5: Configure Startup Command

**In App Service → Configuration → General Settings:**
```bash
Startup Command: gunicorn --bind=0.0.0.0 --timeout 600 Aaarohan_Backend.wsgi
```

### Step 6: Database Setup

**Option A: Using Azure Cloud Shell**
```bash
# Connect to your app
az webapp ssh --resource-group SAI-Fitness-RG --name sai-fitness-backend

# Run migrations
python manage.py migrate
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

**Option B: Using Local Connection**
```bash
# Install Azure CLI locally
# Set environment variable DATABASE_URL to Azure PostgreSQL
# Run migrations locally
python manage.py migrate
```

## 🔧 Azure Configuration Files

Your project already includes:
- ✅ `requirements.txt` - Python dependencies
- ✅ `runtime.txt` - Python 3.11 specification
- ✅ Production settings in `settings.py`

## 📱 Your Deployed API

After deployment, your SAI Fitness API will be available at:
```
Base URL: https://sai-fitness-backend.azurewebsites.net/api/

Authentication Endpoints:
- POST /api/auth/register/
- POST /api/auth/login/
- POST /api/auth/token/refresh/
- POST /api/auth/logout/

Athletes & Performance:
- GET /api/athletes/profile/
- POST /api/performance/submit/
- GET /api/leaderboard/

And 19+ more endpoints...
```

## 💰 Azure Pricing

**Recommended for Production:**
- **App Service B1**: $7.30/month (1 core, 1.75GB RAM)
- **PostgreSQL B1ms**: $7.10/month (1 vCore, 2GB RAM)
- **Total**: ~$15/month

**Free Tier Option:**
- **App Service F1**: Free (1GB storage, 60min CPU/day)
- **PostgreSQL**: Use external PostgreSQL service

## 🚀 Alternative: One-Click Azure Deploy

**Use Azure Deploy Button:**
1. Add this to your GitHub README:
```markdown
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/...)
```

## ⚡ Quick Commands Summary

```bash
# 1. Create Resource Group
az group create --name SAI-Fitness-RG --location eastus

# 2. Create App Service Plan
az appservice plan create --name SAI-Fitness-Plan --resource-group SAI-Fitness-RG --sku B1 --is-linux

# 3. Create Web App
az webapp create --resource-group SAI-Fitness-RG --plan SAI-Fitness-Plan --name sai-fitness-backend --runtime "PYTHON|3.11"

# 4. Configure GitHub deployment
az webapp deployment source config --name sai-fitness-backend --resource-group SAI-Fitness-RG --repo-url https://github.com/Adi-Yadav1/Aarohan_Backend --branch main
```

## 🎉 Benefits of Azure Deployment

- ✅ **Auto-scaling** based on demand
- ✅ **SSL certificates** included
- ✅ **Monitoring** and logging built-in
- ✅ **CI/CD** from GitHub automatically
- ✅ **Database backups** included
- ✅ **Global CDN** available
- ✅ **99.95% uptime SLA**

Your SAI Fitness backend will be production-ready with all 19+ API endpoints, JWT authentication, file uploads, and database management!