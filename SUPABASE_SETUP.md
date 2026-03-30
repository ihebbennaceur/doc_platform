# Configuration Supabase PostgreSQL

## 🚀 Étapes de Configuration

### 1. Connexion Supabase
Votre base de données Supabase est configurée avec:
```
Host: db.cuwaspbwlefzvuforuen.supabase.co
Database: postgres
User: postgres
```

### 2. Variables d'Environnement
Votre fichier `.env` contient:
```
DATABASE_URL=postgresql://postgres:UdwEnVpZ9RN/Trz@db.cuwaspbwlefzvuforuen.supabase.co:5432/postgres
```

### 3. Configuration Django
Les deux services Django (backend et doccheck) sont configurés pour:
- **Développement**: Utiliser SQLite (`db.sqlite3`)
- **Production**: Utiliser PostgreSQL via `DATABASE_URL` (Supabase)

### 4. Migration de Base de Données
Une fois l'environnement configuré, exécutez:

**Pour le backend principal:**
```bash
cd backend_django/backend_seller_platform
python manage.py migrate
```

**Pour le doccheck service:**
```bash
cd django/doccheck_service
python manage.py migrate
```

### 5. Test de Connexion
```bash
python manage.py dbshell
```

### 6. Déploiement sur Vercel/Render

**Sur Render ou Railway:**
1. Défini `DATABASE_URL` dans les variables d'environnement
2. Exécutez les migrations au déploiement
3. Django utilisera automatiquement PostgreSQL

**Frontend sur Vercel:**
```
NEXT_PUBLIC_API_URL=https://your-backend.render.com
NEXT_PUBLIC_APP_NAME=PFE Seller Platform
```

## 📝 Notes Importantes

⚠️ **Ne partagez JAMAIS votre `DATABASE_URL` réelle!**
- Le fichier `.env` est dans `.gitignore`
- Utilisez uniquement `.env.example` pour les templates
- Chaque environnement (local, staging, production) doit avoir son propre `.env`

## 🔗 Ressources
- [Supabase Docs](https://supabase.io/docs)
- [Django Database Configuration](https://docs.djangoproject.com/en/6.0/ref/settings/#databases)
- [dj-database-url](https://github.com/jazzband/dj-database-url)
