#!/usr/bin/env python
"""
Prepare and deploy the backend service to Railway.
"""
import json
import os
from pathlib import Path

print("=" * 70)
print("BACKEND SERVICE - RAILWAY DEPLOYMENT SETUP")
print("=" * 70)

# Load environment variables
env_file = Path(__file__).parent / '.env.json'

if not env_file.exists():
    print("❌ .env.json not found!")
    exit(1)

with open(env_file) as f:
    env_data = json.load(f)

backend_vars = env_data.get('backend', {})

print("\n" + "=" * 70)
print("BACKEND ENVIRONMENT VARIABLES FOR RAILWAY")
print("=" * 70)

for key, value in backend_vars.items():
    # Hide sensitive values
    if any(secret in key.lower() for secret in ['key', 'secret', 'password', 'token']):
        display_value = f"{value[:10]}...{value[-5:]}" if len(value) > 15 else "***"
    else:
        display_value = value
    
    print(f"{key}={display_value}")

print("\n" + "=" * 70)
print("DEPLOYMENT STEPS:")
print("=" * 70)

print("""
1. Go to https://railway.app/dashboard
2. Click your project
3. Click "+ New" to add a new service
4. Select "Deploy from GitHub"
5. Select "doc_platform" repository
6. Wait for deployment to start

7. Go to Variables tab
8. Add all variables from above (copy exact values!)

9. Go to Deployments tab
10. Click "Redeploy"

11. Wait 2-3 minutes for build and deployment

12. Go to Overview tab
13. Copy the public URL
14. Test:
    - https://[URL]/api/schema/     (should download YAML)
    - https://[URL]/api/docs/       (should show Swagger UI)
    - https://[URL]/api/redoc/      (should show ReDoc)
""")

print("\n" + "=" * 70)
print("DOCKERFILE CONFIGURATION")
print("=" * 70)

print("""
The Dockerfile.backend is already configured:
✓ Port: 8080 (Railway standard)
✓ Path: Dockerfile.backend (in project root)
✓ Django app: myproject (from backend_django/backend_seller_platform/myproject)

If Railway doesn't auto-detect, set:
- Dockerfile Path: Dockerfile.backend
- Build Context: . (root)
""")

print("\n" + "=" * 70)
print("AFTER DEPLOYMENT:")
print("=" * 70)

print("""
1. Run migrations (if needed):
   railway run python manage.py migrate

2. Create admin user (if needed):
   railway run python manage.py createsuperuser

3. Test API endpoints in Swagger UI

4. Note the backend URL for frontend integration
""")

print("\n✅ Backend is ready for deployment!")
print("📌 Copy the variables from above and add them to Railway dashboard.\n")
