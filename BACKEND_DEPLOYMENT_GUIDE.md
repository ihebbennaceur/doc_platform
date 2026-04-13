# Deux Services Backend - Vue d'Ensemble

## 📊 Architecture Finale

```
Railway Project (pfe_seller_platform)
│
├─ Service 1: DocCheck Microservice ✅ DÉPLOYÉ
│  ├─ URL: https://doccheckservice-copy-production.up.railway.app
│  ├─ Port: 8080
│  ├─ Repo: doc_check_service
│  ├─ Endpoints:
│  │  ├─ /api/docs/          → Swagger UI
│  │  ├─ /api/redoc/         → ReDoc
│  │  ├─ /api/schema/        → OpenAPI JSON
│  │  └─ /api/cases/*        → Document verification endpoints
│  └─ Status: ✅ Online
│
└─ Service 2: Backend API (À DÉPLOYER)
   ├─ URL: https://[YOUR-URL].up.railway.app
   ├─ Port: 8080
   ├─ Repo: doc_platform
   ├─ Endpoints:
   │  ├─ /api/docs/          → Swagger UI
   │  ├─ /api/redoc/         → ReDoc
   │  ├─ /api/schema/        → OpenAPI JSON
   │  ├─ /admin/             → Django Admin
   │  └─ /api/accounts/*     → User management
   │  └─ /api/documents/*    → Document management
   │  └─ /api/payments/*     → Payment processing
   └─ Status: ⏳ Ready to deploy
```

---

## 🚀 Déployer le Backend

### Étape 1: Créer le Service Railway

1. Va sur **https://railway.app/dashboard**
2. Clique sur ton **projet**
3. Clique sur **"+ New"** pour ajouter un nouveau service
4. Choisis **"Deploy from GitHub"**
5. Sélectionne le repo **`doc_platform`**
6. Clique **"Deploy"**

Railway va commencer à builder l'image depuis `Dockerfile.backend`.

### Étape 2: Configurer les Variables

Une fois le service créé (2-3 min):

1. Clique sur le **service backend** (pas doccheck)
2. Va à l'onglet **"Variables"**
3. Ajoute **toutes ces variables** (depuis `.env.json` section "backend"):

```
DJANGO_SECRET_KEY=your-super-secret-key-backend-change-this-in-production-12345678901234567890
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,doc-production-xxxx.up.railway.app,.railway.app
DATABASE_URL=postgresql://postgres:UdwEnVpZ9RN@db.cuwaspbwlefzvuforuen.supabase.co:5432/postgres
AWS_ACCESS_KEY_ID=AKIAXDP3XZQGYHZC7JZJ
AWS_SECRET_ACCESS_KEY=3UqV7qsH/RrQDUhKgLVCvCzd8y7Q9d8q+ZF7L8k9M0N1O2P3Q4R5
AWS_STORAGE_BUCKET_NAME=doc-check-iheb
AWS_S3_REGION_NAME=eu-west-1
STATIC_URL=/static/
MEDIA_URL=/media/
```

### Étape 3: Redeploy avec les Variables

1. Va à l'onglet **"Deployments"**
2. Clique **"Redeploy"**
3. Attends 2-3 minutes

### Étape 4: Vérifier les Logs

1. Va à l'onglet **"Logs"**
2. Tu devrais voir:
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8080
[INFO] Using worker: sync
[INFO] Booting worker with pid: 2
```

### Étape 5: Tester l'URL

1. Va à **"Overview"**
2. Copie l'URL publique
3. Teste:
```
https://[URL]/api/schema/        ← Doit télécharger YAML
https://[URL]/api/docs/          ← Doit montrer Swagger UI
https://[URL]/api/redoc/         ← Doit montrer ReDoc
```

---

## 📋 Checklist de Déploiement

Backend:
- [ ] Créer le service Railway
- [ ] Ajouter toutes les variables d'env
- [ ] Cliquer Redeploy
- [ ] Vérifier les logs (pas d'erreurs)
- [ ] Tester /api/schema/
- [ ] Tester /api/docs/
- [ ] Copier l'URL pour le frontend

DocCheck (déjà fait ✅):
- [x] Service en ligne
- [x] Swagger fonctionne
- [x] Endpoints accessibles

---

## 🔗 Intégration Frontend

Une fois les deux services en ligne:

1. **URL du Backend**: `https://[BACKEND-URL]`
2. **URL du DocCheck**: `https://doccheckservice-copy-production.up.railway.app`
3. Configurer le frontend pour appeler les deux services
4. CORS déjà configuré sur les deux backends

---

## 🎯 Prochaines Étapes Après Déploiement

### Pour le Backend:

```bash
# 1. Exécuter les migrations
railway run python manage.py migrate

# 2. Créer un utilisateur admin
railway run python manage.py createsuperuser

# 3. Vérifier Django Admin
https://[BACKEND-URL]/admin/
```

### Pour le Frontend:

```javascript
// Mettre à jour les URLs d'API
const BACKEND_URL = 'https://[BACKEND-URL]';
const DOCCHECK_URL = 'https://doccheckservice-copy-production.up.railway.app';

// Endpoints disponibles:
// GET /api/docs/                 - Documentation Swagger
// GET /api/schema/               - Schéma OpenAPI
// POST /api/accounts/login/      - Login utilisateur
// POST /api/documents/upload/    - Upload document
// POST /api/doccheck/verify/     - Vérifier document (DocCheck service)
```

---

## ✅ Configuration Finale

Quand tout fonctionne:

**DocCheck Service**
- ✅ URL: https://doccheckservice-copy-production.up.railway.app
- ✅ Port: 8080
- ✅ Swagger: https://doccheckservice-copy-production.up.railway.app/api/docs/

**Backend Service**
- ✅ URL: https://[BACKEND-URL]
- ✅ Port: 8080
- ✅ Swagger: https://[BACKEND-URL]/api/docs/

**Frontend Service** (déjà en ligne)
- ✅ URL: https://[FRONTEND-URL] (Vercel)
- ✅ Connecté au backend + doccheck

---

## 🆘 Troubleshooting

### Backend ne répond pas (502)
1. Vérifier le Dockerfile.backend utilise port 8080
2. Vérifier toutes les variables d'env sont présentes
3. Vérifier les Logs pour l'erreur exacte

### Swagger ne s'affiche pas
1. Tester /api/schema/ d'abord
2. Vérifier que drf-spectacular est installé
3. Vérifier les Logs Django

### Base de données erreur
1. Vérifier DATABASE_URL est correct
2. Vérifier Supabase est accessible
3. Exécuter: `railway run python manage.py migrate`

---

## 📞 Support

Si tu bloques:
1. Copy-paste l'erreur exacte des Logs Railway
2. Dis-moi le statut de chaque étape
3. Envoie une screenshot du Railway dashboard
