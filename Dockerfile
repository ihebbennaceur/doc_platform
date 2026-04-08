FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy the doccheck service
COPY django/doccheck_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY django/doccheck_service .

# Create necessary directories
RUN mkdir -p staticfiles media

EXPOSE 8001

# Run gunicorn
CMD ["gunicorn", "doccheck_service.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "3"]
