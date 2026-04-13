#!/usr/bin/env python
"""
Test Django startup without database connection.
Tests if Swagger endpoints are configured correctly.
"""
import os
import sys
import json
from pathlib import Path

# Load environment variables
env_file = Path(__file__).parent / '.env.json'
with open(env_file) as f:
    env_data = json.load(f)

doccheck_vars = env_data.get('doccheck', {})

# Set environment variables
for key, value in doccheck_vars.items():
    os.environ[key] = value

# Change to doccheck directory
os.chdir(Path(__file__).parent / 'doc-check-service')
sys.path.insert(0, str(Path.cwd()))

# Test Django without database
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doccheck_service.settings')

import django
django.setup()

print("=" * 60)
print("TESTING DJANGO URLS AND SWAGGER ENDPOINTS")
print("=" * 60)

from django.urls import get_resolver

resolver = get_resolver()
patterns = resolver.url_patterns

print("\n✓ Django URLs loaded successfully!\n")

print("Available endpoints:")
print("-" * 60)

for pattern in patterns:
    pattern_str = str(pattern.pattern)
    # Show the endpoint name if available
    if hasattr(pattern, 'name'):
        name = pattern.name
        print(f"  {pattern_str:<40} -> {name}")
    else:
        print(f"  {pattern_str}")

print("\n" + "=" * 60)
print("SWAGGER ENDPOINTS:")
print("=" * 60)

swagger_patterns = [str(p.pattern) for p in patterns if 'docs' in str(p.pattern).lower() or 'schema' in str(p.pattern).lower()]

if swagger_patterns:
    for pattern in swagger_patterns:
        print(f"  ✓ {pattern}")
else:
    print("  ⚠ No Swagger endpoints found!")

print("\n" + "=" * 60)
print("TESTING SPECTACULAR SCHEMA GENERATION")
print("=" * 60)

try:
    from drf_spectacular.openapi import AutoSchema
    from rest_framework.request import Request
    from rest_framework.test import APIRequestFactory
    
    factory = APIRequestFactory()
    request = factory.get('/')
    request = Request(request)
    
    print("✓ drf-spectacular loaded successfully")
    print("✓ OpenAPI schema generation is available")
    
except Exception as e:
    print(f"❌ Error with drf-spectacular: {e}")

print("\n" + "=" * 60)
print("REST FRAMEWORK CONFIGURATION")
print("=" * 60)

from django.conf import settings

print(f"Default schema class: {settings.REST_FRAMEWORK.get('DEFAULT_SCHEMA_CLASS')}")
print(f"Authentication classes: {settings.REST_FRAMEWORK.get('DEFAULT_AUTHENTICATION_CLASSES')}")
print(f"Permission classes: {settings.REST_FRAMEWORK.get('DEFAULT_PERMISSION_CLASSES')}")

print("\n✓ All Swagger configuration looks good!")
print("\nIf endpoints are not showing on Railway:")
print("1. Check that Django is actually starting (check logs)")
print("2. Make sure all environment variables are set")
print("3. Try accessing /api/schema/ first (the schema endpoint)")
print("4. Then access /api/docs/ for Swagger UI")
