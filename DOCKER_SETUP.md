# Docker Setup Guide

## Quick Start with Docker Compose

### 1. Build Images
```bash
docker-compose build
```

### 2. Start Services
```bash
docker-compose up -d
```

### 3. View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f doccheck
```

### 4. Access Services
- **Backend API:** http://localhost:8000/api/
- **DocCheck Service:** http://localhost:8001/api/
- **Frontend:** http://localhost:3000 (run `npm run dev` separately)

### 5. Stop Services
```bash
docker-compose down
```

---

## Build Individual Docker Images

### Backend (Port 8000)
```bash
cd backend_django/backend_seller_platform
docker build -t pfe-backend:latest .
docker run -p 8000:8000 \
  -e DEBUG=false \
  -e SECRET_KEY=your-secret-key \
  -e ALLOWED_HOSTS=localhost \
  pfe-backend:latest
```

### DocCheck Service (Port 8001)
```bash
cd django/doccheck_service
docker build -t pfe-doccheck:latest .
docker run -p 8001:8001 \
  -e DEBUG=false \
  -e SECRET_KEY=your-secret-key \
  -e ALLOWED_HOSTS=localhost \
  pfe-doccheck:latest
```

---

## Environment Variables

Create a `.env` file in the repo root:

```
# AWS S3
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret

# API Keys
GOOGLE_API_KEY=your-google-key
DEEPSEEK_API_KEY=your-deepseek-key

# Database (optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@db:5432/pfe_platform
```

---

## Check Images

List all images:
```bash
docker images | grep pfe
```

Expected output:
```
pfe-backend         latest      xxxxx      2.5GB
pfe-doccheck        latest      xxxxx      2.3GB
postgres            15-alpine   xxxxx      75MB
```

---

## Troubleshooting

### Migrations Failed
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec doccheck python manage.py migrate
```

### Port Already in Use
```bash
# Free port 8000
lsof -ti:8000 | xargs kill -9

# Free port 8001
lsof -ti:8001 | xargs kill -9

# Free port 5432
lsof -ti:5432 | xargs kill -9
```

### Clear Everything
```bash
docker-compose down -v
docker-compose build --no-cache
```

---

## Production Deployment

For production, use:
- **Amazon ECS** or **AWS ECR** (recommended)
- **Google Cloud Run**
- **Azure Container Instances**

Push images:
```bash
docker tag pfe-backend:latest myregistry/pfe-backend:latest
docker push myregistry/pfe-backend:latest
```
