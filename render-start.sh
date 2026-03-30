#!/bin/bash
# Render start script for pfe_seller_platform backend
# Root directory is set to backend_django/backend_seller_platform on Render

cd myproject
exec gunicorn backend_seller_platform.wsgi:application --bind 0.0.0.0:${PORT:-8000}
