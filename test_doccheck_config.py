#!/usr/bin/env python
"""
Extract environment variables from .env.json and test Django configuration.
"""
import json
import os
import sys
from pathlib import Path

# Load the .env.json file
env_file = Path(__file__).parent / '.env.json'

if not env_file.exists():
    print("❌ .env.json not found!")
    sys.exit(1)

with open(env_file) as f:
    env_data = json.load(f)

# Get doccheck variables
doccheck_vars = env_data.get('doccheck', {})

print("=" * 60)
print("DOCCHECK ENVIRONMENT VARIABLES FOR RAILWAY")
print("=" * 60)

for key, value in doccheck_vars.items():
    # Hide sensitive values
    if any(secret in key.lower() for secret in ['key', 'secret', 'password', 'token']):
        display_value = f"{value[:10]}...{value[-5:]}" if len(value) > 15 else "***"
    else:
        display_value = value
    
    print(f"{key}={display_value}")

print("\n" + "=" * 60)
print("HOW TO ADD TO RAILWAY:")
print("=" * 60)
print("""
1. Go to https://railway.app/dashboard
2. Click on your project
3. Click on "doccheck-service" 
4. Click the "Variables" tab
5. For each variable above, click "Add Variable" and:
   - Key: [the variable name]
   - Value: [paste the full value from above]

OR use Railway CLI:
""")

print("\nrailway variables set \\")
for key, value in doccheck_vars.items():
    # For CLI, we need to escape values properly
    print(f'  {key}="{value}" \\')

print("\n" + "=" * 60)
print("THEN CLICK 'Redeploy' TO RESTART WITH NEW VARIABLES")
print("=" * 60)

# Test if we can import Django
print("\n" + "=" * 60)
print("TESTING DJANGO IMPORT...")
print("=" * 60)

try:
    os.chdir(Path(__file__).parent / 'doc-check-service')
    sys.path.insert(0, str(Path.cwd()))
    
    # Set env vars for this test
    for key, value in doccheck_vars.items():
        os.environ[key] = value
    
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doccheck_service.settings')
    django.setup()
    
    print("✓ Django imported successfully")
    print("✓ Settings loaded")
    
    # Test database
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("✓ Database connection works!")
    
    # Test S3
    from django.core.files.storage import default_storage
    storage_type = default_storage.__class__.__name__
    print(f"✓ Storage backend: {storage_type}")
    
    # Test URLs
    from django.urls import get_resolver
    resolver = get_resolver()
    patterns = [str(p.pattern) for p in resolver.url_patterns]
    print(f"✓ Swagger endpoints found:")
    for p in patterns:
        if 'api' in p.lower() or 'docs' in p.lower():
            print(f"  - {p}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
