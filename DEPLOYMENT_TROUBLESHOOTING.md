# Deployment Troubleshooting Guide

## Error: "Application failed to respond"

This error typically means the application crashes at startup or cannot bind to the port.

### Possible Causes & Solutions

#### 1. **Missing Environment Variables on Railway** ⚠️ MOST LIKELY
**Problem**: Railway doesn't have the environment variables set.

**Solution**: 
1. Go to Railway dashboard
2. Select the **doccheck-service** deployment
3. Go to **Variables** tab
4. Add these variables:
   - `DATABASE_URL` = your Supabase connection string
   - `AWS_ACCESS_KEY_ID` = your AWS key
   - `AWS_SECRET_ACCESS_KEY` = your AWS secret
   - `AWS_STORAGE_BUCKET_NAME` = "doc-check-iheb"
   - `AWS_S3_REGION_NAME` = "eu-west-1"
   - `DJANGO_SECRET_KEY` = your secret key
   - `DJANGO_DEBUG` = "false"
   - `DJANGO_ALLOWED_HOSTS` = "doccheckservice-copy-production.up.railway.app,.railway.app,localhost"

#### 2. **Port Binding Issue**
**Problem**: Port 8001 might already be in use or not exposed.

**Solution**:
- Check Dockerfile: `EXPOSE 8001` ✅ (already set)
- Check CMD: uses `--bind 0.0.0.0:8001` ✅ (already set)
- Railway should auto-map port 8001 to the service port

#### 3. **Database Connection Error**
**Problem**: Cannot connect to Supabase at startup.

**Solution**:
- Verify `DATABASE_URL` is correct: `postgresql://user:password@host:5432/db`
- Check if Supabase database is running
- Test locally first: `python manage.py shell` should connect

#### 4. **Missing Migrations**
**Problem**: Database tables don't exist.

**Solution** (after Railway starts):
```bash
railway run python manage.py migrate
```
Then restart the service.

#### 5. **Import or Configuration Error**
**Problem**: Python module not found or settings.py has error.

**Solution**:
1. Test locally in Docker:
   ```bash
   docker build -f Dockerfile -t doccheck:test .
   docker run -it doccheck:test /bin/bash
   python manage.py check
   ```

2. Check for circular imports or missing packages
3. Verify all imports in `doccheck_service/settings.py` work

#### 6. **Missing Static Files**
**Problem**: Static files directory doesn't exist.

**Solution**: 
- Dockerfile creates it: `RUN mkdir -p staticfiles media` ✅

### Debugging Steps

**Step 1: Check Local Docker Build**
```bash
cd doc-check-service
docker build -f Dockerfile -t doccheck:debug .
docker run -it -e DATABASE_URL="your_db_url" doccheck:debug
```

**Step 2: View Railway Deployment Logs**
- Go to Railway dashboard
- Select doccheck-service
- Go to **Logs** tab
- Look for error messages

**Step 3: Check Gunicorn Is Starting**
The error "Application failed to respond" often means:
- Gunicorn can't start (port in use or syntax error)
- Gunicorn starts but crashes immediately
- Environment variables missing (ImportError, ConnectionError)

**Step 4: Railway Configuration Check**
- **Start Command**: Should be blank (use Dockerfile CMD)
- **Port**: Should auto-detect 8001
- **Root Directory**: Should be `/app` (Dockerfile WORKDIR)
- **Procfile**: Should NOT exist (using Docker)

### Quick Fixes to Try

1. **Restart the service** in Railway dashboard (Redeploy button)
2. **Clear Docker cache**:
   ```bash
   docker system prune -a
   docker build --no-cache -f Dockerfile -t doccheck:fresh .
   ```
3. **Check Python version**: Dockerfile uses `python:3.11-slim` ✅
4. **Verify requirements.txt**: All packages installable
5. **Test gunicorn command locally**:
   ```bash
   gunicorn doccheck_service.wsgi:application --bind 0.0.0.0:8001 --workers 3 --timeout 120
   ```

### Environment Variables on Railway

Set these in the Railway dashboard (Variables tab):

```
DATABASE_URL=postgresql://...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=doc-check-iheb
AWS_S3_REGION_NAME=eu-west-1
DJANGO_SECRET_KEY=...
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=doccheckservice-copy-production.up.railway.app,.railway.app
```

### Next Steps

1. **Go to Railway Dashboard**
2. **Select DocCheck Service**
3. **Check Variables Tab** - Are all env vars set?
4. **Check Logs Tab** - What's the actual error?
5. **Click Redeploy** to trigger a fresh build
6. **Check Logs Again** - Did it start?

If still failing, reply with the error message from Railway logs.
