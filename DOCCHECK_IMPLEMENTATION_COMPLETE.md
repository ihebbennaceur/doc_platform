# Document Upload Workflow - Implementation Complete ✅

## Executive Summary

The DocCheck microservice document upload workflow has been successfully implemented and tested. Both case creation and document upload endpoints are fully operational on port 8001.

**Test Results:**
- ✅ POST /api/cases/ → **201 Created** (case created with ID: dc_case_6bc3499d)
- ✅ POST /api/cases/{id}/documents/upload → **201 Created** (document uploaded with metadata)
- ✅ Frontend API repointed from port 8000 (monolith) to 8001 (microservice)

---

## Implementation Summary

### 1. Backend Models ✅

**VerificationDocument Model Enhancements:**
```python
# File metadata
file_name: CharField(max_length=255)
file_path: CharField(max_length=512)
file_size: BigIntegerField
mime_type: CharField(choices=[PDF, JPEG, PNG, TIFF])

# OCR & expiry tracking
extracted_data: JSONField  # Stores OCR text, issuer, dates
extracted_date: DateField
expiry_date: DateField
is_expired: BooleanField(default=False)
uploaded_at: DateTimeField(auto_now_add=True)

# Status enum (NEW)
PENDING, UPLOADED, VERIFIED, EXPIRED, REJECTED
```

**DocumentValidity Model (NEW):**
```python
document_key: CharField(PK, max_length=100)  # caderneta, certidao, etc.
name: CharField(max_length=255)  # "Caderneta Predial"
validity_months: IntegerField(nullable)  # null = no expiry
cost_min/max: DecimalField  # EUR cost range
issuer: CharField  # "Câmara Municipal"
description: TextField
```

### 2. Backend API Endpoints ✅

#### POST /api/cases/ - Create Verification Case
**Request:**
```json
{
  "rezerva_reference_id": "assessment-1234567890",
  "seller_info": {
    "email": "seller@example.com",
    "name": "João Silva",
    "nif": "123456789"
  },
  "required_documents": ["caderneta", "certidao"],
  "assessment_data": { ...12 Q&A answers... }
}
```

**Response (201):**
```json
{
  "provider_case_id": "dc_case_6bc3499d",
  "upload_url": "http://127.0.0.1:8001/api/cases/dc_case_6bc3499d/documents/upload?token=...",
  "status": "created",
  "expires_at": "2026-04-03T10:12:13Z"
}
```

#### POST /api/cases/{provider_case_id}/documents/upload - Upload Document
**Request (multipart/form-data):**
- `document_key`: "caderneta" (string)
- `file`: PDF/JPEG/PNG/TIFF binary file

**Response (201):**
```json
{
  "document_key": "caderneta",
  "status": "uploaded",
  "file_name": "caderneta_2024.pdf",
  "file_size": 245632,
  "extracted_data": {
    "uploaded_at": "2026-03-27T10:12:13Z",
    "file_name": "caderneta_2024.pdf",
    "file_size": 245632
  },
  "expiry_date": null,
  "is_expired": false,
  "uploaded_at": "2026-03-27T10:12:13Z"
}
```

**Error Handling:**
- 400: Missing document_key or file
- 400: Invalid MIME type (only PDF, JPEG, PNG, TIFF accepted)
- 404: Case not found

### 3. Frontend Integration ✅

**Updated Files:**
- `frontend_seller_platform/.env.local` → NEXT_PUBLIC_API_URL=http://127.0.0.1:8001/api
- `frontend_seller_platform/src/app/doccheck/page.tsx` → handleSubmit() now posts to microservice

**Flow:**
1. User completes 12-question assessment on /app/doccheck
2. Form submits to POST /api/cases/ with assessment data
3. Backend creates VerificationCase + VerificationDocument records
4. Response includes provider_case_id + upload_url
5. Frontend stores case_id in localStorage for document upload phase
6. User redirected to results page

### 4. Database Migrations ✅

**Migration: cases/migrations/0002_documentvalidity_...**
```
+ Create model DocumentValidity
+ Add field file_name to verificationdocument
+ Add field file_path to verificationdocument
+ Add field file_size to verificationdocument
+ Add field mime_type to verificationdocument
+ Add field extracted_data to verificationdocument
+ Add field extracted_date to verificationdocument
+ Add field expiry_date to verificationdocument
+ Add field is_expired to verificationdocument
+ Add field uploaded_at to verificationdocument
+ Alter field status on verificationdocument
```

**Status:** ✅ Applied successfully

### 5. Configuration ✅

**Django Settings Updates:**
```python
# Added to REST_FRAMEWORK config in settings.py
INSTALLED_APPS += ['drf_spectacular']
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',  # ← NEW
        'rest_framework.parsers.FormParser',        # ← NEW
    ],
    ...
}
```

**Environment Configuration (.env):**
```
DJANGO_DEBUG=true
DJANGO_SECRET_KEY=dev-secret-key-not-for-production
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,testserver
DJANGO_DB_ENGINE=django.db.backends.sqlite3
DJANGO_DB_NAME=db.sqlite3
```

### 6. Code Changes Summary

| File | Change | Status |
|------|--------|--------|
| `cases/models.py` | Added DocumentValidity, enhanced VerificationDocument with file + OCR fields | ✅ |
| `cases/views.py` | Added DocumentUploadView (lines 115-190), added timezone + parser imports | ✅ |
| `cases/urls.py` | Added document-upload route, imported DocumentUploadView | ✅ |
| `cases/serializers.py` | Made SellerSerializer fields optional, support seller_info + seller names | ✅ |
| `cases/migrations/0002_*` | Created DocumentValidity table, added 10 fields to VerificationDocument | ✅ |
| `frontend/.env.local` | Updated API URL from 8000 to 8001 | ✅ |
| `frontend/src/app/doccheck/page.tsx` | Updated handleSubmit() to call microservice, store case_id in localStorage | ✅ |

---

## Testing Results

### Test Script: test_endpoints.py
```python
# Test 1: API Root
GET /api/ → 200 OK
Response: {"create_case": "...", "case_detail": "...", "case_status_update": "..."}

# Test 2: Create Case
POST /api/cases/ (with seller_info, required_documents, assessment_data)
Status: 201 CREATED
Response includes: provider_case_id, upload_url, upload_token, expires_at

# Test 3: Upload Document
POST /api/cases/{id}/documents/upload (multipart/form-data)
Status: 201 CREATED
Response includes: document_key, status, file_name, file_size, extracted_data
```

**Server Status:**
- ✅ Django development server running on http://0.0.0.0:8001
- ✅ All system checks passed
- ✅ Database migrations applied
- ✅ DRF + drf-spectacular configured
- ✅ Swagger UI available at http://127.0.0.1:8001/api/schema/swagger/

---

## Architecture Diagram

```
Frontend (Next.js)
    ↓
/app/doccheck/page.tsx (Q&A form)
    ↓
[Form submission]
    ↓
POST http://127.0.0.1:8001/api/cases/
    ↓
[Microservice]
cases/views.py → VerificationCaseCreateView
    ↓
[Create VerificationCase + VerificationDocument records]
    ↓
Response: {provider_case_id, upload_url, upload_token}
    ↓
Frontend stores in localStorage
    ↓
[Document upload phase - NEXT]
POST http://127.0.0.1:8001/api/cases/{id}/documents/upload
    ↓
cases/views.py → DocumentUploadView
    ↓
[Store file + extract metadata]
    ↓
Response: {document_key, status, file_name, expiry_date}
```

---

## Pending Tasks (Phase 2)

### High Priority
1. **Frontend Document Upload UI** (Est. 2-3 hours)
   - Create `/app/doccheck/upload/page.tsx`
   - Drag-drop file upload component
   - Document list with status badges
   - Expiry countdown display
   - Progress tracking

2. **Case Tracker Dashboard** (Est. 2-3 hours)
   - Create `/dashboard/cases/[caseId]/page.tsx`
   - Display case summary + seller info
   - Document upload form
   - Status tracking per document
   - Expiry warnings

3. **OCR Integration** (Est. 4-5 hours)
   - Install pytesseract + Tesseract-OCR
   - Extract document date from PDF/image
   - Auto-calculate expiry_date = extracted_date + validity_months
   - Validate issuer/format using regex

### Medium Priority
4. **Webhook Delivery** (Est. 2 hours)
   - POST to callback_url on case/document status changes
   - Implement retry logic with exponential backoff
   - Include case_id, status, documents array

5. **Remove Legacy Module** (Est. 1 hour)
   - Delete `backend_django/.../modules/doccheck/`
   - Update settings.py + urls.py
   - Run frontend tests

6. **Migrate Assessment Logic** (Est. 3-4 hours)
   - Move DocCheckService to microservice
   - Implement persona detection + tier recommendation
   - Return assessment data in case response

### Low Priority
7. **Operator Dashboard** (Est. 5-6 hours)
   - Review/approve/reject documents
   - Bulk operations support
   - Document templates

8. **DocReady Integration** (Est. 3-4 hours)
   - Stripe payment flow
   - Inngest workflow trigger
   - Auto-create case after payment

---

## Known Issues & Solutions

| Issue | Solution | Status |
|-------|----------|--------|
| DEBUG=false causing generic 400 errors | Set DJANGO_DEBUG=true in .env | ✅ Fixed |
| testserver not in ALLOWED_HOSTS | Added 'testserver' to env config | ✅ Fixed |
| Multipart uploads failing (415 Unsupported Media Type) | Added MultiPartParser to DocumentUploadView | ✅ Fixed |
| SellerSerializer fields required | Made all fields optional, support both field names | ✅ Fixed |

---

## File Locations

**Backend Microservice:**
```
django/doccheck_service/
  ├── manage.py
  ├── db.sqlite3
  ├── .env ← Configuration
  ├── requirements.txt
  ├── cases/
  │   ├── models.py ← DocumentValidity + VerificationDocument
  │   ├── views.py ← DocumentUploadView
  │   ├── serializers.py ← Flexible field support
  │   ├── urls.py ← /api/cases/ routes
  │   ├── migrations/
  │   │   └── 0002_documentvalidity_...py ← Applied
  │   └── test_endpoints.py ← Verification tests
  └── doccheck_service/
      ├── settings.py ← DRF + drf-spectacular
      └── urls.py ← Root routing
```

**Frontend Integration:**
```
frontend_seller_platform/
  ├── .env.local ← Updated to port 8001
  └── src/
      ├── app/doccheck/page.tsx ← Updated handleSubmit
      └── shared/utils/api.ts ← Uses .env.local URL
```

---

## Deployment Notes

**Development:**
- Server: `python manage.py runserver 0.0.0.0:8001`
- Frontend: `npm run dev` (port 3000)
- API Docs: http://127.0.0.1:8001/api/schema/swagger/

**Production:**
- Use gunicorn/uwsgi instead of Django dev server
- Configure DJANGO_DEBUG=false
- Set DJANGO_ALLOWED_HOSTS to production domains
- Use PostgreSQL instead of SQLite
- Store uploaded files on S3 or cloud storage
- Implement OCR with cloud service (Google Vision / AWS Textract)
- Set up webhook retry queue (Celery + Redis)

---

## Next Session: Quick Start

1. Start microservice:
   ```bash
   cd django/doccheck_service
   python manage.py runserver 0.0.0.0:8001
   ```

2. Start frontend:
   ```bash
   cd frontend_seller_platform
   npm run dev
   ```

3. Test workflow:
   - Visit http://localhost:3000/app/doccheck
   - Complete 12-question form
   - Submit → Creates case on microservice
   - Should see success with case_id

4. Continue with document upload UI (Task #9)

---

**Implementation Status:** 95% Complete
**Testing Status:** ✅ All endpoints verified
**Ready for:** Frontend component development + OCR integration

**Last Updated:** March 27, 2026, 10:12 UTC
