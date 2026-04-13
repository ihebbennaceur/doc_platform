# 🚀 Configuration Finale - Frontend + Backend Integration

## ✅ Architecture Déployée

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION                               │
├─────────────────────────────────────────────────────────────┤
│ Frontend (Vercel)                                           │
│ https://docfrontend-beta.vercel.app                         │
│ ├─ API Client → Backend                                     │
│ └─ API Client → DocCheck Service                            │
├─────────────────────────────────────────────────────────────┤
│ Backend API (Railway)                                       │
│ https://backenddoccheck-production.up.railway.app/api       │
│ ├─ User Authentication                                      │
│ ├─ Document Management                                      │
│ ├─ Orders & Payments                                        │
│ └─ SmartCMA Reports                                         │
├─────────────────────────────────────────────────────────────┤
│ DocCheck Service (Railway)                                  │
│ https://doccheckservice-copy-production.up.railway.app/api  │
│ └─ Document Verification                                    │
├─────────────────────────────────────────────────────────────┤
│ Database (Supabase PostgreSQL)                              │
│ postgresql://...@db.cuwaspbwlefzvuforuen.supabase.co        │
├─────────────────────────────────────────────────────────────┤
│ Storage (AWS S3)                                            │
│ s3://doc-check-iheb (eu-west-1)                             │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Configuration Actuelle

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://backenddoccheck-production.up.railway.app/api
NEXT_PUBLIC_DOCCHECK_API_URL=https://doccheckservice-copy-production.up.railway.app/api
```

### Backend CORS (settings.py)
```python
CORS_ALLOWED_ORIGINS = [
    'https://docfrontend-beta.vercel.app',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
```

### Backend ALLOWED_HOSTS (env variable)
```
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app,docfrontend-beta.vercel.app,.vercel.app
```

## 🔧 Mise à jour Railway

### Étape 1: Ouvrir Railway Dashboard
1. Go to https://railway.app
2. Login avec ton compte
3. Select le projet

### Étape 2: Backend Service - backenddoccheck-production

1. Click sur le service "backenddoccheck-production"
2. Go to "Variables" tab
3. Ajouter/mettre à jour ces variables:

```
DJANGO_SECRET_KEY=your-super-secret-key-backend-change-this-in-production-12345678901234567890
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app,docfrontend-beta.vercel.app,.vercel.app
DATABASE_URL=postgresql://postgres:UdwEnVpZ9RN@db.cuwaspbwlefzvuforuen.supabase.co:5432/postgres
AWS_ACCESS_KEY_ID=AKIAXDP3XZQGYHZC7JZJ
AWS_SECRET_ACCESS_KEY=3UqV7qsH/RrQDUhKgLVCvCzd8y7Q9d8q+ZF7L8k9M0N1O2P3Q4R5
AWS_STORAGE_BUCKET_NAME=doc-check-iheb
AWS_S3_REGION_NAME=eu-west-1
STATIC_URL=/static/
MEDIA_URL=/media/
```

4. Click "Deploy" to redeploy with new variables

### Étape 3: DocCheck Service - doccheckservice-copy-production

1. Click sur le service "doccheckservice-copy-production"
2. Go to "Variables" tab
3. Ajouter/mettre à jour ces variables:

```
DJANGO_SECRET_KEY=your-super-secret-key-doccheck-change-this-in-production-12345678901234567890
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app,docfrontend-beta.vercel.app,.vercel.app
DATABASE_URL=postgresql://postgres:UdwEnVpZ9RN@db.cuwaspbwlefzvuforuen.supabase.co:5432/postgres
AWS_ACCESS_KEY_ID=AKIAXDP3XZQGYHZC7JZJ
AWS_SECRET_ACCESS_KEY=3UqV7qsH/RrQDUhKgLVCvCzd8y7Q9d8q+ZF7L8k9M0N1O2P3Q4R5
AWS_STORAGE_BUCKET_NAME=doc-check-iheb
AWS_S3_REGION_NAME=eu-west-1
STATIC_URL=/static/
MEDIA_URL=/media/
```

4. Click "Deploy" to redeploy with new variables

## ✅ Vérification

### 1. Test Frontend
```
https://docfrontend-beta.vercel.app
```
- Should load without CORS errors
- Can navigate to /auth/register

### 2. Test Backend Health
```
curl https://backenddoccheck-production.up.railway.app/health/
```
Expected response:
```json
{"status": "ok"}
```

### 3. Test Backend API Docs
```
https://backenddoccheck-production.up.railway.app/api/docs/
```
Should load Swagger UI

### 4. Test DocCheck API Docs
```
https://doccheckservice-copy-production.up.railway.app/api/docs/
```
Should load Swagger UI

## 🔗 API Endpoints Available

### Backend API
- `POST /api/token/` - Obtain JWT token
- `POST /api/register/` - User registration
- `GET/POST /api/documents/` - Document management
- `GET/POST /api/orders/` - Order management
- `POST /api/payments/` - Payment operations
- `GET/POST /api/cma/` - CMA reports
- `GET/POST /api/doccheck/` - Document checking

### DocCheck API
- `POST /api/cases/` - Create verification case
- `GET /api/cases/{id}/` - Get case details
- `POST /api/cases/{id}/documents/upload` - Upload document
- `PUT /api/cases/{id}/status/` - Update status

## 📱 Frontend Features

- ✅ User Authentication (Register/Login)
- ✅ Document Upload & Management
- ✅ Order Management
- ✅ Payment Processing
- ✅ DocCheck Integration
- ✅ Document Verification
- ✅ Dashboard

## 🎯 Next Steps

1. **Deploy Backend** → Railway redeploy with new variables
2. **Deploy DocCheck** → Railway redeploy with new variables
3. **Test Integration** → Frontend → Backend → Database
4. **Monitor Logs** → Check Railway logs for any errors
5. **Test Full Flow** → Register → Upload Doc → Verify

## 🆘 Troubleshooting

### CORS Error
- Check `DJANGO_ALLOWED_HOSTS` includes `.vercel.app`
- Check CORS_ALLOWED_ORIGINS includes `https://docfrontend-beta.vercel.app`
- Redeploy backend after changing

### 502 Bad Gateway
- Check Railway service is running
- Check environment variables are set
- Check logs in Railway dashboard

### Frontend Can't Connect
- Check NEXT_PUBLIC_API_URL points to correct backend
- Check frontend is deployed on Vercel
- Check backend is accepting CORS from Vercel domain

---

✅ **Configuration Complete!** Ready for full integration testing.
