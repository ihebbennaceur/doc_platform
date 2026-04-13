#!/usr/bin/env python
"""
Run Django migrations on Railway backend service.
Execute this script to apply all database migrations.
"""
import os
import sys
import django
from pathlib import Path

# Get the directory
script_dir = Path(__file__).parent
backend_dir = script_dir / 'backend_django' / 'backend_seller_platform' / 'myproject'

# Add to path
sys.path.insert(0, str(backend_dir))
os.chdir(str(backend_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

print("=" * 70)
print("RUNNING DJANGO MIGRATIONS")
print("=" * 70)

try:
    django.setup()
    print("✓ Django setup complete\n")
    
    from django.core.management import call_command
    
    # Run migrations
    print("Running: python manage.py migrate")
    print("-" * 70)
    call_command('migrate', verbosity=2)
    print("-" * 70)
    
    print("\n✓ Migrations completed successfully!")
    print("\nYour API should now work at:")
    print("https://backenddoccheck-production.up.railway.app/api/docs/")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
