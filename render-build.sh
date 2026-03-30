#!/bin/bash
# Render build script for pfe_seller_platform backend

set -e

echo "Installing dependencies..."
cd backend_django/backend_seller_platform
pip install -r requirements.txt

echo "Running migrations..."
cd myproject
python manage.py migrate --noinput

echo "Build completed successfully"
