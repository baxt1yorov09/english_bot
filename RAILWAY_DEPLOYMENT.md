# Railway Deployment Guide

## 1. GitHub Repository
1. Create new repository on GitHub
2. Push your code to GitHub:
```bash
git init
git add .
git commit -m "Initial commit - CEFR Bot"
git branch -M main
git remote add origin https://github.com/username/cefr-bot.git
git push -u origin main
```

## 2. Railway Deployment
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Railway will auto-detect your project

## 3. Environment Variables
In Railway dashboard, add these variables:
- `TELEGRAM_BOT_TOKEN`: Your bot token
- `SECRET_KEY`: Django secret key (generate one)
- `DEBUG`: False
- `DJANGO_SETTINGS_MODULE`: cefr_bot.settings
- `ALLOWED_HOSTS`: railway.app

## 4. Database Setup
Railway will automatically create PostgreSQL database.
The `DATABASE_URL` will be auto-added to your environment.

## 5. Deployment
- Railway will automatically deploy on push to main branch
- Check logs in Railway dashboard
- Your bot will be available at: `your-project-name.railway.app`

## 6. Custom Domain (Optional)
1. Go to Settings → Domains
2. Add your custom domain
3. Update DNS records

## 7. Monitoring
- Check logs in Railway dashboard
- Set up uptime monitoring (UptimeRobot)
- Monitor resource usage

## Files Created:
- `Procfile` - Tells Railway how to run your app
- `railway.toml` - Railway configuration
- `.env.example` - Environment variables template

## Important Notes:
- Remove real bot token from code before pushing to GitHub
- Use environment variables for all sensitive data
- Railway provides free PostgreSQL database
- Automatic restart on failure
