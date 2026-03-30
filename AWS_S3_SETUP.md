# AWS S3 Configuration Guide

## 📦 S3 Bucket Setup

Your S3 bucket is configured with:
```
Bucket Name: doc-check-iheb
Region: eu-west-1
Upload Path: s3://doc-check-iheb/upload-docs/
```

## 🔑 AWS Credentials

Your credentials are stored in `.env` (NOT committed to GitHub):
```
AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>
AWS_STORAGE_BUCKET_NAME=doc-check-iheb
AWS_S3_REGION_NAME=eu-west-1
```

⚠️ **IMPORTANT**: 
- Never commit `.env` to GitHub (it's in `.gitignore`)
- Never share your AWS credentials
- Credentials are only for local development and production deployment secrets

## 🚀 How It Works

### Automatic Detection
Django automatically detects if S3 is configured:
- **If `AWS_ACCESS_KEY_ID` is set** → Uses S3 for document storage
- **If `AWS_ACCESS_KEY_ID` is NOT set** → Uses local `/media` folder

### Document Upload Flow
1. User uploads document via frontend
2. Django receives file via `/api/documents/`
3. File automatically uploads to S3 bucket
4. Database stores S3 URL in `Document.file` field
5. Documents are served directly from S3 CDN

### Media URLs
- Development (local): `http://127.0.0.1:8000/media/documents/filename.pdf`
- Production (S3): `https://doc-check-iheb.s3.eu-west-1.amazonaws.com/media/documents/filename.pdf`

## 📝 S3 Bucket Policies

Make sure your S3 bucket has the correct policy for public read access:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::doc-check-iheb/*"
    }
  ]
}
```

## 🧪 Testing S3 Upload

### Local Testing
1. Ensure `.env` has AWS credentials (see `.env.example` for template)

2. Start backend:
   ```bash
   cd backend_django/backend_seller_platform
   python manage.py runserver
   ```

3. Upload a document via API:
   ```bash
   POST http://localhost:8000/api/documents/
   - file: (multipart form data)
   - document_type: IDENTITY_CARD
   ```

4. Check S3 bucket - file should appear in AWS console

## ⚙️ Production Deployment

### Render/Railway Deployment
1. Set environment variables in deployment platform:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_STORAGE_BUCKET_NAME`
   - `AWS_S3_REGION_NAME`

2. Django will automatically use S3 if credentials are present

3. No need to manage local media files (they're all on S3)

## 🔗 Useful Links
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [django-storages Documentation](https://django-storages.readthedocs.io/)
- [AWS IAM User Management](https://console.aws.amazon.com/iam/)

## 🛡️ Security Notes

✅ **DO:**
- Keep credentials in `.env` (which is in `.gitignore`)
- Use IAM roles with minimal permissions for production
- Enable S3 bucket versioning
- Enable S3 encryption at rest

❌ **DON'T:**
- Commit `.env` to GitHub
- Share AWS credentials publicly
- Use root AWS account (use IAM user)
- Make bucket completely public (use signed URLs for sensitive files)
