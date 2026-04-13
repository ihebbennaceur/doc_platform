# Railway - Configuration Détaillée des Variables

## 🔴 PROBLÈME IDENTIFIÉ

Tu dis "j'ai mis les infos dans secret pour les variables" mais les endpoints ne s'affichent pas. 

**C'est probablement parce que Railway n'expose pas correctement les variables ou il y a une erreur de formatage.**

---

## ✅ SOLUTION: Vérifier la Configuration Railway Pas à Pas

### ÉTAPE 1: Aller au Dashboard Railway

1. Ouvre https://railway.app/dashboard
2. Clique sur ton **projet**
3. Tu dois voir 2 services:
   ```
   [Your Project]
   ├── backend
   └── doccheck-service
   ```
4. **Clique sur "doccheck-service"**

### ÉTAPE 2: Vérifier les Variables

1. Clique sur l'onglet **"Variables"**
2. Tu devrais voir une liste comme:
   ```
   DJANGO_SECRET_KEY: [masked value]
   DJANGO_DEBUG: false
   DJANGO_ALLOWED_HOSTS: localhost,127.0.0.1,...
   DATABASE_URL: [masked value]
   AWS_ACCESS_KEY_ID: [masked value]
   ...
   ```

**⚠️ SI TU VOIS RIEN** → Il y a un problème!

### ÉTAPE 3: Ajouter/Vérifier les Variables Correctement

Si les variables ne sont pas là, il faut les ajouter manuellement:

**Voici les 10 variables à ajouter:**

```
Clé: DJANGO_SECRET_KEY
Valeur: your-super-secret-key-doccheck-change-this-in-production-12345678901234567890

Clé: DJANGO_DEBUG
Valeur: false

Clé: DJANGO_ALLOWED_HOSTS
Valeur: localhost,127.0.0.1,doccheck-production-xxxx.up.railway.app,.railway.app

Clé: DATABASE_URL
Valeur: postgresql://postgres:UdwEnVpZ9RN@db.cuwaspbwlefzvuforuen.supabase.co:5432/postgres

Clé: AWS_ACCESS_KEY_ID
Valeur: AKIAXDP3XZQGYHZC7JZJ

Clé: AWS_SECRET_ACCESS_KEY
Valeur: 3UqV7qsH/RrQDUhKgLVCvCzd8y7Q9d8q+ZF7L8k9M0N1O2P3Q4R5

Clé: AWS_STORAGE_BUCKET_NAME
Valeur: doc-check-iheb

Clé: AWS_S3_REGION_NAME
Valeur: eu-west-1

Clé: STATIC_URL
Valeur: /static/

Clé: MEDIA_URL
Valeur: /media/
```

### ÉTAPE 4: Cliquer sur "Redeploy"

1. Va à l'onglet **"Deployments"**
2. Tu verras une liste de déploiements
3. Clique sur le bouton **"Redeploy"** pour le déploiement actuel
4. Attends **2-3 minutes**

### ÉTAPE 5: Vérifier les Logs

1. Va à l'onglet **"Logs"**
2. Tu devrais voir:
   ```
   [2026-04-10 07:49:43 +0000] [1] [INFO] Starting gunicorn 21.2.0
   [2026-04-10 07:49:43 +0000] [1] [INFO] Listening at: http://0.0.0.0:8001 (1)
   [2026-04-10 07:49:43 +0000] [1] [INFO] Using worker: sync
   [2026-04-10 07:49:43 +0000] [2] [INFO] Booting worker with pid: 2
   ```

**✓ Si tu vois ces logs** → Django démarre correctement!

### ÉTAPE 6: Tester les URLs

1. Va à l'onglet **"Overview"**
2. Tu verras une URL publique (ex: `https://doccheckservice-copy-production.up.railway.app`)
3. Teste ces URLs dans le navigateur:

   **Test 1: Vérifier que le serveur répond**
   ```
   https://doccheckservice-copy-production.up.railway.app/
   ```
   Tu devrais voir une page d'erreur (c'est normal, y'a pas de route `/`)

   **Test 2: Voir le schéma OpenAPI en JSON**
   ```
   https://doccheckservice-copy-production.up.railway.app/api/schema/
   ```
   Tu devrais voir du JSON avec tous les endpoints

   **Test 3: Voir Swagger UI**
   ```
   https://doccheckservice-copy-production.up.railway.app/api/docs/
   ```
   Tu devrais voir l'interface Swagger interactive!

---

## 🆘 Troubleshooting

### ❌ Je ne vois rien (Page blanche ou erreur)

**Cause 1: Django crash au démarrage**
- Va à Logs tab
- Copy-paste l'erreur exacte ici
- Je vais la corriger

**Cause 2: Variables mal formatées**
- Vérifie que tu as copié-collé exactement les valeurs
- Pas d'espaces avant/après
- Pas de guillemets supplémentaires

**Cause 3: Port pas ouvert**
- Check: Dockerfile doit avoir `EXPOSE 8001` ✓
- Check: CMD doit avoir `--bind 0.0.0.0:8001` ✓

### ❌ Erreur 500 (Internal Server Error)

Va à Logs et envoie-moi l'erreur exacte.

Probablement:
- `django.db.utils.ProgrammingError` = Migrations pas appliquées
- `ImportError` = Package manquant dans requirements.txt
- `KeyError` = Variable d'environnement manquante

### ❌ Swagger page vide / No endpoints

Possible causes:
1. Django démarre mais ne charge pas les URLs
2. drf-spectacular n'est pas activé
3. SPECTACULAR_SETTINGS n'est pas bon

Solution: Envoie le log exact de Railway.

---

## 📝 RÉSUMÉ RAPIDE

1. ✓ Variables ajoutées dans Railway Dashboard
2. ✓ Clique Redeploy
3. ✓ Attends 2-3 min
4. ✓ Check Logs
5. ✓ Test `/api/schema/` (doit retourner JSON)
6. ✓ Test `/api/docs/` (doit montrer Swagger)

**Si `/api/schema/` retourne du JSON, c'est bon! Swagger va marcher!**

---

## 🎯 PROCHAINES ÉTAPES

Après avoir configuré Railway:
1. **Exécute migrations** (si besoin): `railway run python manage.py migrate`
2. **Crée un utilisateur admin** (si besoin): `railway run python manage.py createsuperuser`
3. **Test les endpoints** dans Swagger UI
4. **Configure le backend** de la même façon

**Envoie-moi une screenshot des Logs si ça ne marche pas!**
