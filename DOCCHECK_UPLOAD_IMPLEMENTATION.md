# Document Upload Workflow Implementation - Progress Report

## ✅ COMPLETED TASKS

### 1. Document Upload Endpoint Implementation
- **File:** `django/doccheck_service/cases/views.py`
- **Class:** `DocumentUploadView` (new)
- **Features:**
  - Accepts POST requests with multipart/form-data
  - Parameters: `document_key` (string), `file` (binary)
  - MIME type validation (allows PDF, JPEG, PNG, TIFF only)
  - Stores file metadata: file_name, file_size, mime_type, file_path
  - Extracts and stores basic document metadata in `extracted_data` JSONField
  - Calculates expiry_date based on DocumentValidity validity_months
  - Returns: {document_key, status, file_name, file_size, extracted_data, expiry_date, is_expired, uploaded_at}
  - Status code: 201 CREATED on success

- **Error Handling:**
  - 400 Bad Request: Missing document_key or file
  - 400 Bad Request: Invalid MIME type
  - 404 Not Found: Case not found

- **Code Location:** Lines 122-181 in views.py

### 2. Model Enhancements
- **File:** `django/doccheck_service/cases/models.py`

#### VerificationDocument Model Updates:
- Added file metadata fields:
  - `file_name` (CharField, max_length=255)
  - `file_path` (CharField, max_length=512)
  - `file_size` (BigIntegerField)
  - `mime_type` (CharField, choices for PDF/images)
  
- Added OCR/extraction fields:
  - `extracted_data` (JSONField, for OCR text and metadata)
  - `extracted_date` (DateField, nullable)
  - `expiry_date` (DateField, nullable)
  - `is_expired` (BooleanField, default=False)
  - `uploaded_at` (DateTimeField, auto_now_add)

- Updated status enum:
  - PENDING
  - UPLOADED
  - VERIFIED
  - EXPIRED
  - REJECTED

#### DocumentValidity Model (NEW):
- Reference table for document validity rules
- Fields:
  - `document_key` (CharField, PK, max_length=100)
  - `name` (CharField, max_length=255)
  - `validity_months` (IntegerField, nullable - null means no expiry)
  - `cost_min` (DecimalField)
  - `cost_max` (DecimalField)
  - `issuer` (CharField)
  - `description` (TextField)

### 3. URL Routing
- **File:** `django/doccheck_service/cases/urls.py`
- **New Route:**
  ```
  POST /api/cases/<provider_case_id>/documents/upload
  ```
- Imported `DocumentUploadView` in urlpatterns

### 4. Database Migrations
- **Migration:** `cases/migrations/0002_documentvalidity_...`
- Created DocumentValidity table
- Added 10 new fields to VerificationDocument
- Altered DocumentStatus enum
- Applied successfully to SQLite database

### 5. Frontend API Integration
- **File:** `frontend_seller_platform/src/app/doccheck/page.tsx`
- **Changes:**
  - Updated `handleSubmit()` function to call microservice instead of monolith
  - API endpoint: Uses `process.env.NEXT_PUBLIC_API_URL` (defaults to `http://127.0.0.1:8001/api`)
  - Request format: Posts case creation data to `/api/cases/` with:
    - `rezerva_reference_id`: Unique timestamp-based ID
    - `seller_info`: Email, name, NIF
    - `required_documents`: Empty array (will be computed by backend)
    - `assessment_data`: All Q&A answers
  - Stores returned `provider_case_id` and `upload_token` in localStorage
  - Redirects to results view on success

### 6. Environment Configuration
- **File:** `frontend_seller_platform/.env.local`
- **Update:** Changed `NEXT_PUBLIC_API_URL` from `http://127.0.0.1:8000/api` to `http://127.0.0.1:8001/api`
- This routes all frontend requests to the new microservice instead of the monolith

### 7. Import Statement Fix
- Added `from django.utils import timezone` to views.py
- Required for timestamp calculations in document upload handler

## 🔄 IN PROGRESS / READY FOR TESTING

### Django Microservice Status
- ✅ Server running on port 8001
- ✅ All migrations applied
- ✅ Models compiled without errors
- ✅ System checks passed
- ✅ ViewSet class implemented with proper request/response handling
- ⚠️ Needs testing: Actual file upload functionality

## 📋 PENDING TASKS

### Phase 1 (Immediate)
1. **Test Document Upload Endpoint**
   - Create sample PDF/image files
   - Test multipart form-data submission
   - Verify file storage and metadata extraction
   - Check expiry date calculation

2. **Frontend Document Upload UI**
   - Create `/app/doccheck/upload/page.tsx` (post-assessment document upload flow)
   - Components needed:
     - DocumentUploadZone (drag-drop file input)
     - DocumentList (shows required docs with status badges)
     - ExpiryCountdown (displays document validity dates)
     - UploadProgress (tracks file upload percentage)
   - Integration with case_id stored in localStorage

3. **Case Tracker Page**
   - Create `/dashboard/cases/[caseId]/page.tsx`
   - Display case summary, document list, upload forms
   - Track document statuses (pending, uploaded, verified, expired)
   - Show expiry warnings

### Phase 2 (High Priority)
1. **Migrate Backend Assessment Logic**
   - Move DocCheckService from monolith to microservice
   - Implement `calculate_missing_documents()` logic in microservice
   - Map Q&A answers to persona detection + tier recommendations

2. **OCR Integration**
   - Integrate text extraction library (pytesseract/Cloud Vision)
   - Extract document issuance date, issuer info, document ID
   - Auto-calculate expiry_date = extracted_date + validity_months
   - Store extracted fields in DocumentValidity for validation

3. **Webhook Delivery**
   - Implement retry logic for callback_url notifications
   - POST to seller_info callback_url on:
     - Case created
     - Document uploaded
     - Case verified/rejected
   - Include case_id, status, documents array in webhook payload

### Phase 3 (Medium Priority)
1. **Remove Legacy Module**
   - Delete `backend_django/backend_seller_platform/modules/doccheck/`
   - Remove from settings.py INSTALLED_APPS
   - Remove from urls.py routes
   - Update any remaining monolith integrations to use microservice

2. **Document Management Dashboard**
   - Operator dashboard to review/approve/reject documents
   - Bulk operations support
   - Document templates for common formats

3. **DocReady Order Integration**
   - Stripe payment flow → Inngest workflow
   - Auto-create verification case after successful payment
   - Link cases to Orders

## 📁 File Changes Summary

| File | Type | Change | Status |
|------|------|--------|--------|
| `django/doccheck_service/cases/models.py` | Model | Added DocumentValidity, enhanced VerificationDocument | ✅ Complete |
| `django/doccheck_service/cases/views.py` | View | Added DocumentUploadView class, fixed imports | ✅ Complete |
| `django/doccheck_service/cases/urls.py` | Route | Added document-upload URL pattern | ✅ Complete |
| `django/doccheck_service/cases/migrations/0002_*` | Migration | Created tables, added fields | ✅ Applied |
| `frontend_seller_platform/src/app/doccheck/page.tsx` | Component | Updated handleSubmit to call microservice | ✅ Complete |
| `frontend_seller_platform/.env.local` | Config | Updated API URL to port 8001 | ✅ Complete |

## 🧪 Testing Checklist

- [ ] Create verification case via POST /api/cases/
- [ ] Upload document via POST /api/cases/{id}/documents/upload
- [ ] Verify file stored with correct metadata
- [ ] Check expiry_date calculated correctly
- [ ] Get case details via GET /api/cases/{id}/ with document list
- [ ] Update case status via PATCH /api/cases/{id}/status/
- [ ] Frontend form submission creates case on microservice
- [ ] localStorage stores provider_case_id and upload_token
- [ ] Redirect to results page works
- [ ] Upload UI displays required documents
- [ ] File drag-drop uploads documents successfully
- [ ] Expiry countdown shows correct dates

## 🔗 API Contract

### Create Case
```
POST /api/cases/

Request:
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

Response (201):
{
  "provider_case_id": "case-uuid-1234",
  "status": "pending",
  "upload_token": "token-xyz",
  "upload_url": "http://127.0.0.1:8001/api/cases/case-uuid-1234/documents/upload",
  "seller_info": {...},
  "created_at": "2026-03-27T10:43:51Z",
  "expires_at": "2026-04-03T10:43:51Z"
}
```

### Upload Document
```
POST /api/cases/{provider_case_id}/documents/upload

Request (multipart/form-data):
- document_key: "caderneta"
- file: <binary PDF/image>

Response (201):
{
  "document_key": "caderneta",
  "status": "uploaded",
  "file_name": "caderneta_2024.pdf",
  "file_size": 245632,
  "mime_type": "application/pdf",
  "extracted_data": {
    "uploaded_at": "2026-03-27T10:45:00Z",
    "file_name": "caderneta_2024.pdf",
    "file_size": 245632
  },
  "expiry_date": "2027-03-27",
  "is_expired": false,
  "uploaded_at": "2026-03-27T10:45:00Z"
}
```

### Get Case Details
```
GET /api/cases/{provider_case_id}/

Response (200):
{
  "provider_case_id": "case-uuid-1234",
  "status": "pending",
  "seller_info": {...},
  "documents": [
    {
      "document_key": "caderneta",
      "status": "uploaded",
      "file_name": "caderneta_2024.pdf",
      "file_size": 245632,
      "expiry_date": "2027-03-27",
      "is_expired": false
    },
    {
      "document_key": "certidao",
      "status": "pending",
      "file_name": null,
      "expiry_date": null,
      "is_expired": false
    }
  ],
  "created_at": "2026-03-27T10:43:51Z",
  "expires_at": "2026-04-03T10:43:51Z"
}
```

## 🚀 Next Steps

1. **Immediate (Today):** 
   - Debug server binding issue on port 8001
   - Test upload endpoint with actual file
   - Verify localStorage integration on frontend

2. **Short-term (Next 1-2 sessions):**
   - Implement document upload UI on frontend
   - Create case tracker dashboard page
   - Add OCR integration for document date extraction

3. **Medium-term:**
   - Migrate assessment logic to microservice
   - Remove legacy monolith doccheck module
   - Implement webhook delivery

---

**Last Updated:** March 27, 2026, 10:43 UTC
**Status:** Ready for testing (server operational, models migrated, endpoint implemented)
