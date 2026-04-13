#!/usr/bin/env python
"""
Test migrations without database connection.
Show migration files that need to be applied.
"""
import os
import sys
import django
from pathlib import Path

# Setup path
script_dir = Path(__file__).parent
backend_dir = script_dir / 'backend_django' / 'backend_seller_platform' / 'myproject'
sys.path.insert(0, str(backend_dir))
os.chdir(str(backend_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

print("=" * 70)
print("CHECKING MIGRATIONS")
print("=" * 70)

try:
    django.setup()
    
    from django.core.management import call_command
    from io import StringIO
    
    # Show what migrations exist
    print("\n1. Listing all migrations:")
    print("-" * 70)
    call_command('showmigrations', verbosity=2)
    
    print("\n" + "=" * 70)
    print("If migrations show [ ] (unchecked), they need to be applied on Railway.")
    print("The init.sh script should do this automatically on Railway startup.")
    print("=" * 70)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
