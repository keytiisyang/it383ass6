# Deployment Guide: Render

This guide walks you through deploying the Photo Album Management System to Render.

## Prerequisites

- GitHub account with the project repository pushed
- Cloudinary account (for media storage)
- Render account (free tier available)

## Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Photo Album Management System"
git remote add origin https://github.com/YOUR_USERNAME/it383ass6.git
git branch -M main
git push -u origin main
```

## Step 2: Create Cloudinary Account & Get Credentials

1. Go to [Cloudinary](https://cloudinary.com/)
2. Sign up (free tier is fine)
3. Go to Dashboard → Settings → API Environment Variable
4. Copy the full `CLOUDINARY_URL` (includes api_key, api_secret, cloud_name)
   - Format: `cloudinary://api_key:api_secret@cloud_name`

## Step 3: Deploy to Render

### Option A: Using `render.yaml` (One-Click)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Blueprint** (or **Web Service** for manual config)
3. Connect your GitHub repository
4. Select the branch (usually `main`)
5. Render auto-detects `render.yaml` and configures:
   - Web service with gunicorn
   - PostgreSQL database
   - Build & start commands
6. Set environment variables:
   - `CLOUDINARY_URL`: Paste your Cloudinary URL from Step 2
   - `ALLOWED_HOSTS`: Will be auto-set to your Render domain (e.g., `photo-album-xyz.onrender.com`)
7. Click **Deploy** and wait ~5-10 minutes

### Option B: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Web Service**
3. Connect GitHub repository
4. Configure:
   - **Name**: `photoalbum` (or your choice)
   - **Environment**: `Python 3.11`
   - **Build Command**: 
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**: 
     ```
     gunicorn photoalbum.wsgi
     ```
5. Add environment variables:
   - `SECRET_KEY`: (Render generates automatically)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app.onrender.com` (or use `*` for development)
   - `CLOUDINARY_URL`: (from Step 2)
   - `USE_CLOUDINARY`: `True`
   - `DATABASE_URL`: (Render auto-links from PostgreSQL)
6. Create a PostgreSQL database:
   - Click **New +** → **PostgreSQL**
   - Name: `photoalbum-db`
   - Render links `DATABASE_URL` automatically
7. Click **Create Web Service** and wait for deployment

## Step 4: Verify Deployment

1. Once deployed, go to your app URL (e.g., `https://photoalbum-xyz.onrender.com/`)
2. You should see the Photo Albums page
3. Create a superuser for the admin panel:
   ```bash
   # On your local machine (connected to production DB):
   DATABASE_URL=<render-database-url> python manage.py createsuperuser
   ```
   OR via Render Shell:
   - Open Render dashboard → your web service
   - Click **Shell** tab
   - Run: `python manage.py createsuperuser`
4. Access admin at: `https://your-app.onrender.com/admin/`

## Step 5: Upload Images

1. Log in at `/admin/`
2. Create an album
3. Add photos (images upload directly to Cloudinary)
4. View albums at `/albums/`

## Troubleshooting

### "Database does not exist"
- Wait 2-3 minutes for PostgreSQL to fully initialize
- Check Render logs: **Logs** tab on your service

### "CLOUDINARY_URL not set"
- Verify environment variable is set in Render dashboard
- Redeploy after adding it: Click **Manual Deploy** → **Deploy latest commit**

### Images not loading
- Ensure `USE_CLOUDINARY=True` in production
- Check Cloudinary API credentials in `CLOUDINARY_URL`
- Verify upload was successful in Cloudinary dashboard

### "Not Found (404)" pages
- Ensure `ALLOWED_HOSTS` includes your Render domain (e.g., `photo-album-xyz.onrender.com`)
- Redeploy after updating

## Environment Variables Reference

| Variable | Local Dev | Production | Notes |
|----------|-----------|------------|-------|
| `SECRET_KEY` | Any string | Auto-generated | Keep secret in production |
| `DEBUG` | `True` | `False` | Never `True` in production |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | Your Render domain | Prevents Host header attacks |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Render PostgreSQL URL | Auto-linked by Render |
| `CLOUDINARY_URL` | Optional | Required | Get from Cloudinary dashboard |
| `USE_CLOUDINARY` | `False` | `True` | Enable media storage to Cloudinary |

## Backup & Data

- **Database**: Render PostgreSQL is backed up automatically (free tier: 7-day backups)
- **Images**: Stored in Cloudinary (access via dashboard)
- **Local backup**: Export database regularly for safety

## Custom Domain (Optional)

1. In Render dashboard → your service → **Settings**
2. Scroll to **Custom Domains**
3. Add your domain (e.g., `photos.example.com`)
4. Update DNS records as instructed
5. Wait for SSL certificate (typically 5-10 minutes)

## Next Steps

- Add role-based features (Album Admin group)
- Customize templates with your branding
- Monitor Render logs for issues
- Scale to paid plan if traffic increases
