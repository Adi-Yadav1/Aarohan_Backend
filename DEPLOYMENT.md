# SAI Fitness Backend - Railway Deployment Guide

## 🚀 Fastest Deployment Method: Railway

Railway is the fastest and easiest way to deploy your SAI Fitness backend. It provides:
- ✅ One-click deployment from GitHub
- ✅ Automatic PostgreSQL database setup
- ✅ Free SSL certificates
- ✅ Environment variable management
- ✅ Automatic builds and deployments

## 📋 Prerequisites

1. **GitHub Account** - Your code needs to be in a GitHub repository
2. **Railway Account** - Sign up at [railway.app](https://railway.app)
3. **Cloudinary Account** - For media storage (sign up at [cloudinary.com](https://cloudinary.com))

## 🎯 Step-by-Step Deployment

### Step 1: Push Your Code to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "SAI Fitness Backend - Ready for deployment"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/sai-fitness-backend.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy on Railway

1. **Go to [railway.app](https://railway.app)** and sign in with GitHub
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your SAI Fitness repository**
5. **Railway will automatically detect Django and start deployment!**

### Step 3: Add PostgreSQL Database

1. **In your Railway project dashboard**
2. **Click "New Service" → "Database" → "PostgreSQL"**
3. **Railway will automatically create `DATABASE_URL` environment variable**

### Step 4: Configure Environment Variables

In Railway project settings, add these environment variables:

```env
# Django Settings
SECRET_KEY=your-super-secret-key-here-make-it-random
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app

# Cloudinary (Get from cloudinary.com dashboard)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key  
CLOUDINARY_API_SECRET=your_api_secret

# Email (Optional - for password reset)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=SAI Fitness <your-email@gmail.com>
```

### Step 5: Run Database Migrations

1. **In Railway dashboard, open your service**
2. **Go to "Deploy" tab**
3. **Click "View Logs" to see deployment**
4. **Once deployed, run migrations:**

```bash
# Railway will run these automatically, but you can trigger manually:
python manage.py migrate
python manage.py collectstatic --noinput
```

### Step 6: Create Superuser (Optional)

```bash
# In Railway console or locally with production database:
python manage.py createsuperuser
```

## 🔧 Configuration Files Already Created

Your project already has these deployment files:

- ✅ `requirements.txt` - All Python dependencies
- ✅ `Procfile` - Tells Railway how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `settings.py` - Production-ready configuration

## 📱 API Endpoints Available

Your SAI Fitness backend provides 19+ REST API endpoints:

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login  
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/password-reset-confirm/` - Confirm password reset

### Athletes & Profiles
- `GET /api/athletes/profile/` - Get user profile
- `PUT /api/athletes/profile/` - Update user profile
- `POST /api/athletes/register/` - Register as athlete
- `GET /api/athletes/` - List all athletes

### Performance & Tests
- `GET /api/tests/` - Available fitness tests
- `POST /api/performance/submit/` - Submit performance data
- `GET /api/performance/history/` - Performance history
- `GET /api/performance/analytics/` - Performance analytics

### Leaderboards & Rankings
- `GET /api/leaderboard/` - Global leaderboard
- `GET /api/leaderboard/events/<event_id>/` - Event-specific leaderboard

### Badges & Achievements
- `GET /api/badges/` - Available badges
- `GET /api/badges/my-badges/` - User's earned badges

### Notifications
- `GET /api/notifications/` - User notifications
- `PUT /api/notifications/<id>/read/` - Mark notification as read

## 🌐 Your Deployed API Base URL

After deployment, your API will be available at:
```
https://your-app-name.railway.app/api/
```

## 🔍 Testing Your Deployment

```bash
# Test your deployed API
curl https://your-app-name.railway.app/api/tests/

# Should return list of available fitness tests
```

## ⚡ Alternative Quick Options

If you need even faster deployment:

### Option 1: Heroku (Similar to Railway)
- Create Heroku account
- Install Heroku CLI
- `heroku create your-app-name`
- `git push heroku main`

### Option 2: Render (Free tier available)
- Connect GitHub repo at render.com
- Automatic deployments on code changes

### Option 3: DigitalOcean App Platform
- One-click Django deployment
- $5/month for production apps

## 🎉 You're Done!

Once deployed, your SAI Fitness backend will be live with:
- ✅ Full REST API (19+ endpoints)
- ✅ JWT Authentication
- ✅ PostgreSQL Database
- ✅ File Upload (Cloudinary)
- ✅ Email Notifications
- ✅ Admin Interface
- ✅ Production Security Settings

Your React Native frontend can now connect to the deployed API endpoints!