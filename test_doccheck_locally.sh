#!/bin/bash
# Test Django locally with Railway-like environment

# Load .env.json and set environment variables
export DJANGO_SECRET_KEY="your-super-secret-key-doccheck-change-this-in-production-12345678901234567890"
export DJANGO_DEBUG="false"
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,doccheck-production-xxxx.up.railway.app,.railway.app"
export DATABASE_URL="postgresql://postgres:UdwEnVpZ9RN@db.cuwaspbwlefzvuforuen.supabase.co:5432/postgres"
export AWS_ACCESS_KEY_ID="AKIAXDP3XZQGYHZC7JZJ"
export AWS_SECRET_ACCESS_KEY="3UqV7qsH/RrQDUhKgLVCvCzd8y7Q9d8q+ZF7L8k9M0N1O2P3Q4R5"
export AWS_STORAGE_BUCKET_NAME="doc-check-iheb"
export AWS_S3_REGION_NAME="eu-west-1"
export STATIC_URL="/static/"
export MEDIA_URL="/media/"

cd doc-check-service

echo "=== Testing Django Check ==="
python manage.py check

echo ""
echo "=== Testing Database Connection ==="
python manage.py shell -c "from django.db import connection; print('✓ Database connected successfully'); connection.ensure_connection()"

echo ""
echo "=== Testing S3 Configuration ==="
python manage.py shell -c "from django.core.files.storage import default_storage; print('✓ S3 storage configured'); print(f'Storage: {default_storage}')"

echo ""
echo "=== Testing Swagger Schema ==="
python manage.py shell -c "from django.urls import get_resolver; resolver = get_resolver(); print('✓ URLs loaded'); print([p.pattern for p in resolver.url_patterns[:5]])"

echo ""
echo "=== All Tests Complete ==="
