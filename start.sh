#!/bin/bash
set -e

# For Railway deployment - runs the Docker image
# The image handles the rest (gunicorn startup, etc)

echo "Starting DocCheck service on port 8001..."
exec gunicorn doccheck_service.wsgi:application --bind 0.0.0.0:8001 --workers 3
