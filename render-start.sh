#!/bin/bash
# Render start script for pfe_seller_platform backend

cd backend_django/backend_seller_platform/myproject
exec gunicorn backend_seller_platform.wsgi:application --bind 0.0.0.0:$PORT
