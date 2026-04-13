# ⚙️ Mise à Jour Vercel - Frontend Configuration

## 🎯 Configuration Vercel (Déjà Faite)

Le frontend sur Vercel utilise les variables:

```
NEXT_PUBLIC_API_URL=https://backenddoccheck-production.up.railway.app/api
NEXT_PUBLIC_DOCCHECK_API_URL=https://doccheckservice-copy-production.up.railway.app/api
```

**Status**: ✅ Les variables sont incluses dans le code source (fichier `.env.local`)
- Frontend Vercel auto-redeploie quand on push des changements
- Pas besoin de configurer dans Vercel Dashboard

## 📍 Vérification Frontend

```bash
# Vercel automatically redeploy les changements du repo GitHub
# Il suffit d'attendre quelques minutes après le push
```

**URL**: https://docfrontend-beta.vercel.app

---

# 🚂 Mise à Jour Railway - Backend Configuration

## 📋 Service 1: Backend API - backenddoccheck-production

### Étapes:
1. Go to: https://railway.app
2. Login avec ton compte Railway
3. Ouvre ton projet
4. Clique sur le service **"backenddoccheck-production"**
5. Onglet **"Variables"**
6. Ajoute ou mets à jour ces variables:

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

7. Clique **"Deploy"** pour redéployer

### Vérification:
```
https://backenddoccheck-production.up.railway.app/health/
```
Devrait retourner: `{"status": "ok"}`

---

## 📋 Service 2: DocCheck API - doccheckservice-copy-production

### Étapes:
1. Go to: https://railway.app
2. Login avec ton compte Railway
3. Ouvre ton projet
4. Clique sur le service **"doccheckservice-copy-production"**
5. Onglet **"Variables"**
6. Ajoute ou mets à jour ces variables:

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

7. Clique **"Deploy"** pour redéployer

### Vérification:
```
https://doccheckservice-copy-production.up.railway.app/health/
```
Devrait retourner: `{"status": "ok"}`

---

## ✅ Après Redéploiement

### Test 1: Frontend Accessible
```
https://docfrontend-beta.vercel.app
```
✅ Should load without errors

### Test 2: Backend API Docs
```
https://backenddoccheck-production.up.railway.app/api/docs/
```
✅ Should load Swagger UI

### Test 3: DocCheck API Docs
```
https://doccheckservice-copy-production.up.railway.app/api/docs/
```
✅ Should load Swagger UI

### Test 4: CORS Working
Frontend should be able to call:
```javascript
fetch('https://backenddoccheck-production.up.railway.app/api/token/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'test', password: 'test' })
})
```
✅ Should NOT get CORS error

---

## 🎯 Résumé

| Service | URL | Variables | Status |
|---------|-----|-----------|--------|
| Frontend (Vercel) | https://docfrontend-beta.vercel.app | ✅ Auto-configured | Live |
| Backend (Railway) | https://backenddoccheck-production.up.railway.app | ⏳ Manual update needed | Awaiting |
| DocCheck (Railway) | https://doccheckservice-copy-production.up.railway.app | ⏳ Manual update needed | Awaiting |

---

## ❓ Questions?

- **Frontend not loading?** → Check Vercel deployment logs
- **Backend returns 502?** → Check Railway environment variables
- **CORS error?** → Check DJANGO_ALLOWED_HOSTS includes `.vercel.app`
- **Static files missing?** → Check STATIC_URL and MEDIA_URL variables

---

✅ **Prêt à déployer!**
