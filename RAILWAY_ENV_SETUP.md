# Railway - Configuration des Variables d'Environnement

## 🚀 Comment configurer Railway (Pas à Pas)

### Étape 1: Aller au Dashboard Railway
1. Va sur https://railway.app/dashboard
2. Connecte-toi avec ton compte
3. Clique sur ton **projet** (pfe_seller_platform ou autre nom)

### Étape 2: Sélectionner le Service DocCheck
1. Tu dois voir 2 services: **backend** et **doccheck-service**
2. **Clique sur "doccheck-service"**

### Étape 3: Ouvrir l'onglet Variables
1. En haut de la page, tu vas voir plusieurs onglets:
   - Overview
   - **Variables** ← CLIQUE ICI
   - Logs
   - Settings
   - Deployments
2. **Clique sur l'onglet "Variables"**

### Étape 4: Ajouter les Variables
Tu verras une interface avec des champs pour ajouter des variables.

**Ajoute ces variables une par une** (copie-les exactement depuis ton `.env.json`):

```
DJANGO_SECRET_KEY: your-super-secret-key-doccheck-change-this-in-production-12345678901234567890

DJANGO_DEBUG: false

DJANGO_ALLOWED_HOSTS: localhost,127.0.0.1,doccheck-production-xxxx.up.railway.app,.railway.app

DATABASE_URL: postgresql://postgres:UdwEnVpZ9RN@db.cuwaspbwlefzvuforuen.supabase.co:5432/postgres

AWS_ACCESS_KEY_ID: AKIAXDP3XZQGYHZC7JZJ

AWS_SECRET_ACCESS_KEY: 3UqV7qsH/RrQDUhKgLVCvCzd8y7Q9d8q+ZF7L8k9M0N1O2P3Q4R5

AWS_STORAGE_BUCKET_NAME: doc-check-iheb

AWS_S3_REGION_NAME: eu-west-1

STATIC_URL: /static/

MEDIA_URL: /media/
```

### Étape 5: Cliquer sur "Redeploy"
1. Après avoir ajouté toutes les variables
2. Va à l'onglet **Deployments**
3. Tu verras le dernier déploiement avec un bouton **"Redeploy"**
4. **Clique sur "Redeploy"** pour relancer le service avec les nouvelles variables

### Étape 6: Vérifier les Logs
1. Va à l'onglet **Logs**
2. Tu devrais voir:
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8001 (1)
[INFO] Booting worker with pid: 2
[INFO] Booting worker with pid: 3
[INFO] Booting worker with pid: 4
```
3. Si tu vois ces messages = ✅ SUCCÈS!

### Étape 7: Accéder au Service
Une fois que Gunicorn démarre:
1. Va à l'onglet **Overview**
2. Tu verras une URL comme:
   - `https://doccheckservice-copy-production.up.railway.app`
3. **Ajoute `/api/docs/`** à la fin:
   - `https://doccheckservice-copy-production.up.railway.app/api/docs/`
4. Tu devrais voir **Swagger UI** avec tous les endpoints!

---

## 📍 Où trouver quoi sur Railway

### Vue d'ensemble:
```
railway.app/dashboard
    ↓
[Ton Projet]
    ├── Backend Service
    │   ├── Overview (URL du service)
    │   ├── Variables (env vars)
    │   ├── Logs (console output)
    │   └── Deployments (redeploy)
    │
    └── DocCheck Service
        ├── Overview (URL du service)
        ├── Variables (env vars) ← TU ES ICI
        ├── Logs (console output)
        └── Deployments (redeploy)
```

### Accéder au Port 8001:
- Railway **expose automatiquement** le port 8001
- Tu accèdes via l'URL publique + chemin:
  - `/api/docs/` pour Swagger
  - `/api/redoc/` pour ReDoc
  - `/api/schema/` pour le schéma JSON

---

## ✅ Checklist de Configuration

- [ ] Aller sur railway.app/dashboard
- [ ] Cliquer sur le projet
- [ ] Sélectionner "doccheck-service"
- [ ] Cliquer sur onglet "Variables"
- [ ] Ajouter toutes les 10 variables
- [ ] Cliquer "Redeploy"
- [ ] Aller à l'onglet "Logs" et vérifier que Gunicorn démarre
- [ ] Aller à "Overview" et copier l'URL
- [ ] Ajouter `/api/docs/` à l'URL
- [ ] Ouvrir dans le navigateur
- [ ] Voir Swagger UI ✅

---

## 🆘 Si ça ne marche toujours pas

1. **Vérifier les Logs**:
   - Railway → DocCheck Service → Logs
   - Cherche les messages d'erreur en rouge
   - Copy-paste l'erreur

2. **Vérifier les Variables**:
   - Assure-toi que **TOUS** les `DJANGO_` et `AWS_` sont présents
   - Pas d'espaces inutiles

3. **Redeploy à nouveau**:
   - Clique Deployments → Redeploy
   - Attends 2-3 minutes

4. **Vérifier le Port**:
   - Railway détecte automatiquement le port du Dockerfile (8001)
   - Pas besoin de le configurer manuellement

---

## 📌 Rappel

**Variables d'Environnement** = informations secrètes qu'on donne à Railway sans les mettre dans le code:
- Clés AWS (pour S3)
- URL de la base de données (Supabase)
- Secret key de Django
- etc.

Railway les injecte dans le conteneur au lancement.
