# 🚀 EmotionEye Deployment Guide

## Quick Deploy Options

### 1. Heroku (Recommended)
```bash
# Install Heroku CLI first
heroku create your-app-name
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

### 2. Railway
```bash
# Install Railway CLI
railway login
railway new
railway up
```

### 3. Render
1. Connect GitHub repo to Render
2. Select "Web Service"
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn main:app`

### 4. Google Cloud
```bash
gcloud app deploy
```

### 5. AWS Elastic Beanstalk
```bash
eb init
eb create
eb deploy
```

## Environment Variables
Set these in your deployment platform:
- `FLASK_ENV=production`
- `FLASK_DEBUG=False`
- `PORT=5000` (auto-set by most platforms)

## Files Ready for Deployment:
- ✅ Procfile (Heroku)
- ✅ requirements.txt (Dependencies)
- ✅ runtime.txt (Python version)
- ✅ app.yaml (Google Cloud)
- ✅ main.py (Entry point)
- ✅ Dockerfile (Container deployment)

Your app will be live at: `https://your-app-name.platform.com`