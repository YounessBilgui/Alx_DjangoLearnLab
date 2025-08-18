# Deployment Guide: social_media_api

## 1. Prerequisites
- Python 3.8+
- Git
- Heroku CLI (for Heroku deployment)

## 2. Environment Variables
Set these in your Heroku dashboard or `.env` file:
- `DJANGO_SECRET_KEY`: Your Django secret key
- `DJANGO_DEBUG`: `False`
- `DJANGO_ALLOWED_HOSTS`: Your domain or Heroku app URL (comma-separated)
- `DATABASE_URL`: Heroku Postgres URL (set automatically by Heroku)
- `DJANGO_SECURE_SSL_REDIRECT`: `True`

## 3. Static & Media Files
- Static files are served by Whitenoise (no extra config needed for Heroku)
- For media files, use a service like AWS S3 for production (not required for Heroku demo)

## 4. Deployment Steps (Heroku)
```bash
# Install Heroku CLI and login
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set DJANGO_SECRET_KEY=your-secret-key DJANGO_DEBUG=False DJANGO_ALLOWED_HOSTS=your-app-name.herokuapp.com DJANGO_SECURE_SSL_REDIRECT=True

# Add Heroku Postgres
heroku addons:create heroku-postgresql:hobby-dev

# Push code
git push heroku main

# Run migrations and collectstatic
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput

# Open your app
heroku open
```

## 5. Gunicorn & Procfile
- Gunicorn is used as the WSGI server (see `Procfile`)

## 6. Monitoring & Maintenance
- Use Heroku logs: `heroku logs --tail`
- (Optional) Add Sentry or similar for error monitoring

## 7. Final Testing
- Visit your Heroku app URL and test all endpoints

---
For AWS, DigitalOcean, or custom VPS, see Django docs for production deployment and static/media setup.
