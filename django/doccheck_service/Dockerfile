FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (gcc for psycopg2, postgresql-client, etc)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p staticfiles media

EXPOSE 8001

# Run migrations and start gunicorn
CMD ["gunicorn", "doccheck_service.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "3"]
