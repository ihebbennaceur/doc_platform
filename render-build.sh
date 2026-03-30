#!/bin/bash
# Render build script for pfe_seller_platform backend
# Root directory is set to backend_django/backend_seller_platform on Render

set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
cd myproject
python manage.py migrate --noinput

echo "Build completed successfully"
