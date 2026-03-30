# Developer Handoff - Complete Checklist

## 📦 WHAT TO HAND OFF

### Documentation (Give these files to developer)

- [x] **HANDOFF_READINESS.md** - Overall readiness assessment
- [x] **API_SPECIFICATION.md** - Complete API docs with examples
- [ ] **INTEGRATION_GUIDE.md** - Detailed integration workflow  
- [ ] **DATABASE_SCHEMA.md** - Model relationships
- [ ] **SECURITY_GUIDE.md** - Auth & signing requirements
- [ ] **.env.example** - Configuration template

### Source Code (Ready to review)

```
Backend (DocCheck Service):
✅ /django/doccheck_service/cases/models.py
   - VerificationCase
   - VerificationDocument
   - WebhookEvent
   - DocumentValidity

✅ /django/doccheck_service/cases/views.py
   - VerificationCaseCreateView (POST /api/cases/)
   - DocumentUploadView (POST /api/cases/{id}/documents/upload)
   - VerificationCaseDetailView (GET /api/cases/{id}/)
   - CaseStatusUpdateView (PUT /api/cases/{id}/status/)

✅ /django/doccheck_service/cases/serializers.py
   - All request/response serializers

✅ /django/doccheck_service/cases/urls.py
   - API routing

Frontend (Next.js):
✅ /frontend_seller_platform/src/components/DocumentsManager.tsx
   - Upload UI
   - Document display
   - Extraction trigger

✅ /frontend_seller_platform/src/app/dashboard/page.tsx
   - Dashboard integration
   - Token refresh
```

### Configuration

```
✅ /django/doccheck_service/.env
   - GOOGLE_API_KEY set
   - Ready to add DOCCHECK_API_KEY, REZERVA_PARTNER_KEY

✅ /django/doccheck_service/requirements.txt
   - All dependencies installed

✅ Database
   - Migrations applied
   - Ready for production
```

---

## ✅ WHAT'S WORKING

### Backend API
- ✅ POST /api/cases/ - Create verification case
- ✅ GET /api/cases/{id}/ - Get case details  
- ✅ POST /api/cases/{id}/documents/upload - Upload document
- ✅ PUT /api/cases/{id}/status/ - Update status (internal)

### Frontend
- ✅ Document upload form
- ✅ Document list display
- ✅ Expected field templates
- ✅ Extraction trigger (mock data)
- ✅ Token refresh on auth errors

### Database
- ✅ All models created
- ✅ Migrations applied
- ✅ Indexes on unique fields
- ✅ Foreign key relationships

---

## ⏳ WHAT NEEDS IMPLEMENTATION (HIGH PRIORITY)

### 1. Webhook Delivery Service ⭐ CRITICAL
**File to create:** `/django/doccheck_service/cases/webhook_service.py`

```python
async def send_webhook_to_rezerva(webhook_event: WebhookEvent):
    """
    Requirements:
    - POST to callback_url with payload
    - Retry on timeout/5xx (max 3 attempts)
    - Exponential backoff: 5s → 30s → 5m
    - Do NOT retry on 2xx/4xx
    - Update delivery_status, attempt_count, last_attempt_at
    - Log all attempts
    """
```

**Trigger points:**
- When document status changes (uploaded → present/needs_resolution)
- When overall_status changes (created → in_review/verified/rejected)
- Create WebhookEvent, queue for delivery

**Estimated effort:** 2-3 hours

### 2. Status Management Logic ⭐ IMPORTANT
**File to update:** `/django/doccheck_service/cases/models.py` and `views.py`

**Functions needed:**
```python
def calculate_overall_status(documents: list[VerificationDocument]) -> str:
    """
    Logic:
    - If any 'missing': status = 'in_review'
    - If any 'needs_resolution': status = 'in_review'
    - If all 'present': status = 'verified'
    - If user rejects: status = 'rejected'
    """

def on_document_status_changed(document: VerificationDocument):
    """
    1. Calculate new overall_status
    2. If changed, update VerificationCase.status
    3. Create WebhookEvent with full payload
    4. Queue webhook delivery
    """
```

**Estimated effort:** 1-2 hours

### 3. API Key Authentication ⭐ IMPORTANT
**File to create:** `/django/doccheck_service/cases/auth.py`

```python
def validate_api_key(request):
    """
    1. Extract: Authorization: Bearer <key>
    2. Look up key in database
    3. Return partner info or 401
    
    Apply to:
    - VerificationCaseCreateView
    - VerificationCaseDetailView
    (NOT DocumentUploadView - token-based)
    """

def validate_request_signature(request):
    """Optional but recommended:
    1. Get X-Signature header
    2. Verify HMAC-SHA256 signature
    3. Reject if mismatch
    """
```

**Estimated effort:** 1-2 hours

---

## 📋 DETAILED IMPLEMENTATION CHECKLIST

### Webhook Delivery (Sprint 1)
- [ ] Create `webhook_service.py` with main function
- [ ] Implement retry logic
  - [ ] Exponential backoff
  - [ ] Max 3 attempts
  - [ ] Update database after each attempt
- [ ] Add logging
  - [ ] Log all webhook attempts
  - [ ] Log success/failure
  - [ ] Log error details
- [ ] Create signal handlers
  - [ ] Hook into VerificationDocument.post_save
  - [ ] Trigger status calculation
  - [ ] Queue webhook
- [ ] Create task queue
  - [ ] Celery or APScheduler
  - [ ] Process pending webhooks
  - [ ] Handle retry scheduling
- [ ] Test with mock Rezerva
  - [ ] Simulate 2xx (no retry)
  - [ ] Simulate 5xx (retry)
  - [ ] Simulate timeout (retry)

### Status Management (Sprint 1)
- [ ] Add `calculate_overall_status()` function
- [ ] Add `create_webhook_event()` function
- [ ] Add signal handlers for document changes
- [ ] Update `VerificationCaseDetailView` response to include webhook status
- [ ] Test status transitions
  - [ ] created → in_review → verified
  - [ ] created → in_review → rejected
  - [ ] in_review (partial docs) → in_review (all docs)

### API Key Management (Sprint 2)
- [ ] Create `APIKey` model for partner keys
- [ ] Create admin page for key generation
- [ ] Implement `@require_api_key` decorator
- [ ] Add to VerificationCaseCreateView
- [ ] Add to VerificationCaseDetailView
- [ ] Test with invalid/expired keys
- [ ] Test with valid keys

### Testing & Hardening (Sprint 2)
- [ ] Integration tests
  - [ ] Full flow: create → upload → verify → webhook
  - [ ] Error cases: invalid input, missing files
- [ ] Performance tests
  - [ ] Concurrent uploads
  - [ ] Many webhooks at once
- [ ] Security tests
  - [ ] Invalid API key rejected
  - [ ] Signature validation works
  - [ ] CORS properly configured
- [ ] Monitoring
  - [ ] Error rates tracked
  - [ ] Webhook delivery latency
  - [ ] Failed webhook alerts

---

## 🔧 SETUP FOR DEVELOPER

### Environment
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up .env
cp .env.example .env
# Add to .env:
DOCCHECK_API_KEY=dev-key-12345
REZERVA_PARTNER_KEY=rez-key-12345
WEBHOOK_SECRET=shared-secret-for-signing

# 3. Run migrations
python manage.py migrate

# 4. Create test data
python manage.py shell
from cases.models import APIKey
APIKey.objects.create(key="dev-key-12345", partner="Rezerva", ...)

# 5. Start server
python manage.py runserver 8001
```

### Testing
```bash
# Run existing tests
pytest

# Test webhook delivery
curl -X POST http://localhost:8001/api/cases/ ...

# Mock Rezerva webhook endpoint (for testing)
# Use: https://webhook.site (free)
```

---

## 📞 QUESTIONS FOR DEVELOPER

Before they start:

1. **Task Queue:** Preference - Celery + Redis or APScheduler?
2. **Retry Strategy:** Accept exponential backoff or need different approach?
3. **Monitoring:** Use existing logging or add monitoring service?
4. **Testing:** Mock Rezerva endpoint or use real staging?
5. **Deployment:** Any specific server constraints or policies?

---

## 🚀 GO-LIVE CHECKLIST

Before production:
- [ ] Webhook delivery tested end-to-end
- [ ] Retry logic tested with failures
- [ ] API key management in production
- [ ] Rate limiting implemented
- [ ] Logging to external service (Sentry, CloudWatch, etc)
- [ ] Database backups configured
- [ ] HTTPS enforced
- [ ] Error alerts configured
- [ ] Load testing done (1000+ concurrent uploads)
- [ ] DR/failover plan documented

---

## 📊 SUCCESS CRITERIA

The integration is successful when:

✅ Rezerva can create a case → Receive provider_case_id  
✅ User can upload documents → Files stored securely  
✅ DocCheck verifies → Status updates in case  
✅ Webhook sent → Rezerva receives result  
✅ Webhook retries on failure → Max 3 attempts  
✅ No webhook sent on 4xx errors → No retry spam  
✅ All documents tracked → Status history logged  

---

## ESTIMATE

- **Webhook Delivery:** 2-3 hours
- **Status Management:** 1-2 hours  
- **API Key Auth:** 1-2 hours
- **Testing:** 2-3 hours
- **Documentation:** 1 hour

**Total:** ~8-11 hours (1-2 days for experienced developer)

---

## FILES TO COPY TO DEVELOPER

```
Copy entire folder:
/django/doccheck_service/

Copy for reference:
/frontend_seller_platform/src/components/DocumentsManager.tsx
/backend_django/backend_seller_platform/myproject/accounts/views.py (for token refresh pattern)

Docs:
HANDOFF_READINESS.md
API_SPECIFICATION.md
```

