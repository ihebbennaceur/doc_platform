#!/usr/bin/env python
"""
Update Railway environment variables for both backend services.
This script extracts the correct env vars from .env.json and shows how to update Railway.
"""
import json
from pathlib import Path

env_file = Path(__file__).parent / '.env.json'

with open(env_file) as f:
    env_data = json.load(f)

print("=" * 80)
print("RAILWAY ENVIRONMENT VARIABLES UPDATE")
print("=" * 80)

print("\n" + "=" * 80)
print("1. BACKEND SERVICE - backenddoccheck-production")
print("=" * 80)
backend_vars = env_data.get('backend', {})
print("\nVariables to set in Railway Dashboard:")
print("-" * 80)
for key, value in backend_vars.items():
    print(f"{key}={value}")

print("\n📋 Steps:")
print("1. Go to https://railway.app/project/[PROJECT-ID]/variables")
print("2. Select 'backenddoccheck-production' service")
print("3. Click 'New Variable' for each above")
print("4. Copy-paste the key=value pairs")
print("5. Deploy the service")

print("\n" + "=" * 80)
print("2. DOCCHECK SERVICE - doccheckservice-copy-production")
print("=" * 80)
doccheck_vars = env_data.get('doccheck', {})
print("\nVariables to set in Railway Dashboard:")
print("-" * 80)
for key, value in doccheck_vars.items():
    print(f"{key}={value}")

print("\n📋 Steps:")
print("1. Go to https://railway.app/project/[PROJECT-ID]/variables")
print("2. Select 'doccheckservice-copy-production' service")
print("3. Click 'New Variable' for each above")
print("4. Copy-paste the key=value pairs")
print("5. Deploy the service")

print("\n" + "=" * 80)
print("FRONTEND CONFIGURATION (Vercel)")
print("=" * 80)
print("Frontend URL: https://docfrontend-beta.vercel.app")
print("Backend API: https://backenddoccheck-production.up.railway.app/api")
print("DocCheck API: https://doccheckservice-copy-production.up.railway.app/api")
print("\n✅ Frontend .env.local already configured!")
print("=" * 80)
