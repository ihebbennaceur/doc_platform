# Railway Deployment Guide

## Running Migrations Manually

After deploying on Railway, you need to run migrations manually to set up the database.

### Option 1: Using Railway CLI (Recommended)

```bash
# For DocCheck service
railway run -s doc_check_service python manage.py migrate

# For Backend service  
railway run -s doc_platform python manage.py migrate
```

### Option 2: Using Railway Dashboard

1. Go to your service on Railway dashboard
2. Click on the service → "Shell"
3. Run the migration command:
   ```bash
   python manage.py migrate
   ```

### After First Deployment

When you deploy a new version:

1. Build succeeds first time (no migrations during build)
2. Deploy logs will show gunicorn starting
3. Run migrations using Railway CLI or Dashboard shell
4. Service will be ready to use

### Troubleshooting

If you get "Network is unreachable" error:
- Make sure DATABASE_URL environment variable is set correctly
- Check that Supabase database is accessible from Railway network
- Verify all environment variables are set in Railway dashboard
