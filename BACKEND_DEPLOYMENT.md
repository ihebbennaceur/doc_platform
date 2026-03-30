# Backend Deployment Guide

## Frontend Status ✅
- **Deployed:** https://doc-platform-ten.vercel.app
- **Status:** Live and accessible

## Backend Deployment Instructions

Your backend needs to be deployed to handle API requests from the frontend. Choose one of the options below:

### Option 1: Deploy to Render (Recommended - Free tier available)

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub (easier integration)

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository: `ihebbennaceur/doc_platform`
   - Select repository and connect

3. **Configure Service**
   - **Name:** `pfe-seller-backend`
   - **Region:** Frankfurt (eu-central-1) - closest to your Supabase
   - **Runtime:** Python 3.9+
   - **Root Directory:** `/` (leave as root - repo root)
   - **Build Command:** 
     ```
     bash render-build.sh
     ```
   - **Start Command:**
     ```
     bash render-start.sh
     ```

4. **Set Environment Variables** (in Render Dashboard)
   Copy from `.env` file in your project:
   ```
   DEBUG=false
   SECRET_KEY=<your-django-secret-key>
   ALLOWED_HOSTS=pfe-seller-backend.onrender.com,localhost,127.0.0.1
   DATABASE_URL=<your-supabase-postgresql-url>
   AWS_ACCESS_KEY_ID=<your-aws-access-key>
   AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
   AWS_STORAGE_BUCKET_NAME=doc-check-iheb
   AWS_S3_REGION_NAME=eu-west-1
   CORS_ALLOWED_ORIGINS=https://doc-platform-ten.vercel.app,http://localhost:3000
   ```
   ⚠️ **IMPORTANT:** Never commit `.env` file with secrets to GitHub. Use `.env.example` as template.

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy from GitHub

### Option 2: Deploy to Railway

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Link GitHub repository
   - Select `backend_django/backend_seller_platform` directory

3. **Configure Service**
   - **Build Command:**
     ```
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```
     gunicorn backend_seller_platform.wsgi:application --bind 0.0.0.0:8000
     ```

4. **Set Environment Variables**
   Copy all values from `.env` file (see Render section above for variable names)

5. **Deploy** - Railway auto-deploys

---

## After Backend Deployment

### 1. Update Frontend API URL
Once your backend is deployed, you'll get a URL like:
- Render: `https://pfe-seller-backend.onrender.com`
- Railway: `https://your-project.up.railway.app`

Update in `frontend_seller_platform/.env.local`:
```
NEXT_PUBLIC_API_URL=https://your-backend-url
```

Then redeploy frontend on Vercel (or it will auto-redeploy on git push)

### 2. Test API Connection
```bash
curl https://your-backend-url/api/health/
```

Expected response:
```json
{"status": "ok"}
```

### 3. Test Document Upload
1. Go to https://doc-platform-ten.vercel.app
2. Login with test credentials
3. Upload a document
4. Verify it appears in S3: `https://s3.eu-west-1.amazonaws.com/doc-check-iheb/`

---

## Environment Variables Reference

| Variable | Value | Required |
|----------|-------|----------|
| `DEBUG` | `false` | ✅ |
| `SECRET_KEY` | Your Django secret | ✅ |
| `ALLOWED_HOSTS` | `pfe-seller-backend.onrender.com,localhost` | ✅ |
| `DATABASE_URL` | Supabase PostgreSQL URL | ✅ |
| `AWS_ACCESS_KEY_ID` | S3 Access Key | ✅ |
| `AWS_SECRET_ACCESS_KEY` | S3 Secret Key | ✅ |
| `AWS_STORAGE_BUCKET_NAME` | `doc-check-iheb` | ✅ |
| `AWS_S3_REGION_NAME` | `eu-west-1` | ✅ |
| `CORS_ALLOWED_ORIGINS` | Frontend URL | ✅ |
| `GOOGLE_API_KEY` | For Gemini extraction | ⭕ |
| `DEEPSEEK_API_KEY` | For Deepseek extraction | ⭕ |

---

## Troubleshooting

### Build Fails: `ModuleNotFoundError: No module named 'rest_framework'`
- Ensure `requirements.txt` has all dependencies
- Run: `pip install -r requirements.txt`

### 401 Unauthorized on Frontend
- Check `CORS_ALLOWED_ORIGINS` includes your Vercel domain
- Verify `ALLOWED_HOSTS` includes backend domain
- Check JWT token is being sent: `Authorization: Bearer <token>`

### S3 Upload Fails
- Verify AWS credentials are correct
- Check bucket `doc-check-iheb` exists in `eu-west-1`
- Run: `aws s3 ls s3://doc-check-iheb/`

### Database Connection Fails
- Verify `DATABASE_URL` is correct
- Test connection: `psql postgresql://postgres:...@db.cuwaspbwlefzvuforuen.supabase.co:5432/postgres`
- Ensure Supabase whitelist includes Render/Railway IP

---

## Quick Deploy Checklist

- [ ] Git pushed to GitHub
- [ ] Created Render/Railway account
- [ ] Connected GitHub repository
- [ ] Set all environment variables
- [ ] Service deployed successfully
- [ ] Updated `NEXT_PUBLIC_API_URL` on Vercel
- [ ] Tested API health endpoint
- [ ] Tested document upload flow
