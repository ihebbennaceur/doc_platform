# 📖 Guide des Variables d'Environnement

## 📁 Fichiers Disponibles

### 1. `.env.example` (📚 Documentation)
- **Utilité**: Template de référence
- **Contient**: Toutes les variables nécessaires avec descriptions
- **À faire**: Lire ce fichier pour comprendre quelles variables sont nécessaires
- **Git**: ✅ Commité (pas de secrets)

### 2. `.env.production` (🏭 Production)
- **Utilité**: Configuration de production avec vraies valeurs
- **Contient**: Variables réelles pour Railway et Vercel
- **À faire**: À utiliser comme référence pour configurer les services
- **Git**: ❌ NE PAS commiter (fichier sensible)
- **Note**: Ce fichier est dans `.gitignore`

### 3. `.env.local` (💻 Développement Local)
- **Utilité**: Configuration locale pour développement
- **Contient**: Variables pour tester en local
- **À faire**: Créer et utiliser en développement seulement
- **Git**: ❌ NE PAS commiter (fichier sensible)
- **Localisation**: À la racine du projet ou dans chaque dossier

---

## 🚀 CONFIGURATION RAPIDE

### Pour Railway Backend (backenddoccheck-production)

1. Go to: https://railway.app
2. Select: `backenddoccheck-production` service
3. Tab: `Variables`
4. Ajoute/mets à jour TOUTES ces variables:

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

5. Click: `Deploy`

### Pour Railway DocCheck (doccheckservice-copy-production)

1. Go to: https://railway.app
2. Select: `doccheckservice-copy-production` service
3. Tab: `Variables`
4. Ajoute/mets à jour TOUTES ces variables:

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

5. Click: `Deploy`

### Pour Vercel Frontend (docfrontend-beta)

1. Go to: https://vercel.com
2. Select: `docfrontend-beta` project
3. Settings → `Environment Variables`
4. Ajoute TOUTES ces variables:

```
NEXT_PUBLIC_API_URL=https://backenddoccheck-production.up.railway.app/api
NEXT_PUBLIC_DOCCHECK_API_URL=https://doccheckservice-copy-production.up.railway.app/api
NEXT_PUBLIC_APP_NAME=PFE Seller Platform
NEXT_PUBLIC_APP_VERSION=1.0.0
```

5. Auto-redeployment happens

---

## 💡 Explications

### Pourquoi un `.env.production`?
- **Centralisation**: Toutes les variables au même endroit
- **Référence**: Facile de voir ce qui est configuré
- **Documentation**: Comprendre les dépendances entre services

### Pourquoi `.env.local` pour le développement?
- **Sécurité**: Pas de secrets dans git
- **Flexibilité**: Chaque développeur peut avoir sa config
- **Isolation**: Variables locales ne affect pas production

### Pourquoi pas de `.env` dans les dossiers?
- **Confusion**: Dur de trouver les variables
- **Duplication**: Même variable partout
- **Maintenance**: Difficile à mettre à jour

### Structure Hiérarchique
```
.env.example              ← Template (commité)
.env.production          ← Production (NOT commité)
.env.local               ← Développement local (NOT commité)
.gitignore               ← Exclut les .env sensibles
```

---

## ✅ Checklist Finale

- [ ] `.env.example` lisible et à jour
- [ ] `.env.production` avec vraies valeurs
- [ ] `.env.local` créé pour développement
- [ ] `.gitignore` contient `*.env`, `.env.local`, `.env.production`
- [ ] Railway configuré avec toutes les variables
- [ ] Vercel configuré avec NEXT_PUBLIC_* variables
- [ ] Tests: Frontend peut appeler Backend
- [ ] Tests: Backend peut appeler DocCheck
- [ ] Logs: Aucune erreur CORS

---

## 🔗 Références

- `.env.example` - Voir ce fichier pour template complet
- `.env.production` - Voir ce fichier pour valeurs réelles
- `DEPLOYMENT_CHECKLIST.md` - Instructions étape par étape
- `PUBLIC_ACCESS_DOMAINS.md` - Liste des URLs publiques
- `INTEGRATION_SETUP.md` - Configuration complète
