#!/bin/bash
# Render build script for pfe_seller_platform backend

set -e

echo "Installing dependencies..."
pip install -r backend_django/backend_seller_platform/requirements.txt

echo "Running migrations..."
cd backend_django/backend_seller_platform/myproject
python manage.py migrate --noinput

echo "Build completed successfully"
