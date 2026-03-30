# DocCheck API Specification

**Version:** 1.0  
**Status:** Ready for Integration  
**Base URL:** `http://127.0.0.1:8000/api` (dev) / `https://api.doccheck.com/api` (prod)

---

## 1. POST /cases/ - Create Verification Case

**Called by:** Rezerva  
**Purpose:** Initiate a document verification request

### Request

**Headers:**
```
Authorization: Bearer <DOCCHECK_API_KEY>
Content-Type: application/json
```

**Body:**
```json
{
  "rezerva_reference_id": "rez_docreq_01JXYZ",
  "callback_url": "https://api.rezerva.com/v1/integration/doccheck/update",
  "seller": {
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+351900000000"
  },
  "required_documents": [
    "doc_certidao_permanente",
    "doc_caderneta_predial",
    "doc_licenca_utilizacao",
    "doc_ficha_tecnica",
    "doc_certificado_energetico",
    "doc_registo_predial",
    "doc_cpcv_draft"
  ]
}
```

### Response (201 Created)

```json
{
  "provider_case_id": "dc_case_9a12",
  "upload_url": "https://app.doccheck.com/upload/dc_case_9a12",
  "status": "created",
  "expires_at": "2026-04-02T10:00:00Z"
}
```

### Error Responses

**400 Bad Request** - Missing/invalid fields
```json
{
  "error": "Missing required field: callback_url",
  "code": "INVALID_REQUEST"
}
```

**401 Unauthorized** - Invalid API key
```json
{
  "error": "Invalid or missing API key",
  "code": "AUTH_FAILED"
}
```

**409 Conflict** - Duplicate rezerva_reference_id
```json
{
  "error": "Verification case already exists for this reference",
  "code": "DUPLICATE_CASE"
}
```

---

## 2. GET /cases/{provider_case_id}/ - Get Case Details

**Called by:** Rezerva or frontend  
**Purpose:** Retrieve current status of a verification case

### Request

**Headers:**
```
Authorization: Bearer <DOCCHECK_API_KEY>
```

### Response (200 OK)

```json
{
  "provider_case_id": "dc_case_9a12",
  "rezerva_reference_id": "rez_docreq_01JXYZ",
  "status": "in_review",
  "seller_name": "John Doe",
  "seller_email": "john@example.com",
  "seller_phone": "+351900000000",
  "created_at": "2026-03-26T10:00:00Z",
  "updated_at": "2026-03-26T17:20:00Z",
  "documents": [
    {
      "document_key": "doc_certidao_permanente",
      "status": "present",
      "reason": null,
      "updated_at": "2026-03-26T12:30:00Z"
    },
    {
      "document_key": "doc_caderneta_predial",
      "status": "needs_resolution",
      "reason": "Image is blurry",
      "updated_at": "2026-03-26T17:20:00Z"
    },
    {
      "document_key": "doc_licenca_utilizacao",
      "status": "present",
      "reason": null,
      "updated_at": "2026-03-26T12:35:00Z"
    },
    {
      "document_key": "doc_ficha_tecnica",
      "status": "missing",
      "reason": null,
      "updated_at": "2026-03-26T10:00:00Z"
    },
    {
      "document_key": "doc_certificado_energetico",
      "status": "present",
      "reason": null,
      "updated_at": "2026-03-26T13:00:00Z"
    },
    {
      "document_key": "doc_registo_predial",
      "status": "present",
      "reason": null,
      "updated_at": "2026-03-26T13:15:00Z"
    },
    {
      "document_key": "doc_cpcv_draft",
      "status": "missing",
      "reason": null,
      "updated_at": "2026-03-26T10:00:00Z"
    }
  ]
}
```

### Error Responses

**404 Not Found**
```json
{
  "error": "Case not found",
  "code": "NOT_FOUND"
}
```

---

## 3. POST /cases/{provider_case_id}/documents/upload - Upload Document

**Called by:** User (frontend) - anonymous  
**Purpose:** Upload a document file for the case

### Request

**Headers:**
```
Content-Type: multipart/form-data
```

**Body:**
```
file: <binary PDF/image>
document_key: doc_certidao_permanente
```

### Response (201 Created)

```json
{
  "id": "1",
  "provider_case_id": "dc_case_9a12",
  "document_key": "doc_certidao_permanente",
  "status": "uploaded",
  "file_url": "/media/cases/dc_case_9a12/doc_certidao_permanente/file.pdf",
  "uploaded_at": "2026-03-26T12:30:00Z"
}
```

### Error Responses

**400 Bad Request** - Invalid document type
```json
{
  "error": "Invalid document_key: unknown_type",
  "code": "INVALID_DOCUMENT_TYPE"
}
```

**404 Not Found** - Case doesn't exist
```json
{
  "error": "Case not found",
  "code": "NOT_FOUND"
}
```

**409 Conflict** - Document already uploaded
```json
{
  "error": "Document already uploaded for this case",
  "code": "DUPLICATE_DOCUMENT"
}
```

**413 Payload Too Large** - File too big
```json
{
  "error": "File size exceeds limit (50MB max)",
  "code": "FILE_TOO_LARGE"
}
```

---

## 4. PUT /cases/{provider_case_id}/status/ - Update Case Status (Internal)

**Called by:** DocCheck backend (internal)  
**Purpose:** Update status after verification

### Request

**Body:**
```json
{
  "status": "in_review",
  "documents": {
    "doc_certidao_permanente": {
      "status": "present",
      "reason": null
    },
    "doc_caderneta_predial": {
      "status": "needs_resolution",
      "reason": "Image is blurry"
    }
  }
}
```

### Response (200 OK)

```json
{
  "provider_case_id": "dc_case_9a12",
  "status": "in_review",
  "documents": { ... }
}
```

---

## 5. POST /v1/integration/doccheck/update - Webhook (Callback to Rezerva)

**Called by:** DocCheck → Rezerva  
**Purpose:** Notify Rezerva of verification results

### Request

**Headers:**
```
X-API-KEY: <REZERVA_PARTNER_KEY>
X-Signature: hmac-sha256=<signature>  (optional but recommended)
Content-Type: application/json
```

**Body:**
```json
{
  "rezerva_reference_id": "rez_docreq_01JXYZ",
  "provider_case_id": "dc_case_9a12",
  "event_id": "evt_000001",
  "overall_status": "in_review",
  "documents": {
    "doc_certidao_permanente": "present",
    "doc_caderneta_predial": "needs_resolution",
    "doc_licenca_utilizacao": "present",
    "doc_ficha_tecnica": "missing",
    "doc_certificado_energetico": "present",
    "doc_registo_predial": "present",
    "doc_cpcv_draft": "missing"
  },
  "reason": "Caderneta image is blurry",
  "updated_at": "2026-03-26T17:20:00Z"
}
```

### Expected Response (200 OK)

```json
{
  "ok": true,
  "message": "accepted"
}
```

### Retry Rules

**Retry on:**
- Timeout (> 30s)
- 5xx server errors
- Network errors

**Do NOT retry on:**
- 2xx (already accepted)
- 4xx (validation/auth error)

**Retry strategy:**
- Exponential backoff: 5s → 30s → 5m
- Max 3 attempts
- Log all failures

---

## 6. Status Values

### Per-Document Status
| Status | Meaning | Next Action |
|--------|---------|------------|
| `pending` | Waiting for upload | User must upload file |
| `uploaded` | File received, processing | Verify document |
| `present` | ✅ Document valid | Include in submission |
| `missing` | ❌ User didn't upload | Request re-upload |
| `needs_resolution` | ⚠️ Issues found | User must re-upload |

### Case Status
| Status | Meaning | Transitions |
|--------|---------|------------|
| `created` | Case initialized | → in_review |
| `in_review` | Verification ongoing | → verified or rejected |
| `verified` | ✅ All docs valid | Final state |
| `rejected` | ❌ Cannot verify | Final state |

---

## 7. Error Codes Reference

| Code | HTTP | Meaning |
|------|------|---------|
| `AUTH_FAILED` | 401 | Invalid API key |
| `NOT_AUTHORIZED` | 403 | Not allowed to access this resource |
| `INVALID_REQUEST` | 400 | Missing or invalid required field |
| `INVALID_DOCUMENT_TYPE` | 400 | Unknown document type |
| `DUPLICATE_CASE` | 409 | Case already exists |
| `DUPLICATE_DOCUMENT` | 409 | Document already uploaded |
| `NOT_FOUND` | 404 | Resource not found |
| `FILE_TOO_LARGE` | 413 | File exceeds size limit |
| `SERVER_ERROR` | 500 | Internal server error |

---

## 8. Rate Limiting

```
- Unauthenticated: 10 requests/minute per IP
- Authenticated: 100 requests/minute per API key
- Webhook delivery: No limit (internal)
```

---

## 9. Example Flow

### 1. Rezerva creates case
```
POST /api/cases/
→ Returns: provider_case_id, upload_url
```

### 2. User uploads documents
```
POST /api/cases/{provider_case_id}/documents/upload
→ 3x calls (upload doc_certidao_permanente, etc)
```

### 3. DocCheck verifies
```
Internal: Check uploaded documents
Internal: Calculate overall_status
```

### 4. DocCheck sends webhook
```
POST https://api.rezerva.com/v1/integration/doccheck/update
→ Retry if 5xx/timeout
→ Stop if 2xx/4xx
```

### 5. Rezerva updates records
```
Rezerva stores:
- verification_case: status, updated_at
- doc_verification: per-document status
```

---

## 10. Testing

### Development Endpoint
```
http://127.0.0.1:8000/api/
```

### Test Credentials
```
API_KEY: dev-key-12345
PARTNER_KEY: rez-key-12345 (for Rezerva testing)
```

### Example cURL

```bash
# Create case
curl -X POST http://127.0.0.1:8000/api/cases/ \
  -H "Authorization: Bearer dev-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "rezerva_reference_id": "rez_test_001",
    "callback_url": "https://webhook.site/your-id",
    "seller": {
      "full_name": "Test User",
      "email": "test@example.com",
      "phone": "+351900000000"
    },
    "required_documents": ["doc_certidao_permanente"]
  }'

# Upload document
curl -X POST http://127.0.0.1:8000/api/cases/dc_case_9a12/documents/upload \
  -F "file=@document.pdf" \
  -F "document_key=doc_certidao_permanente"

# Get case status
curl http://127.0.0.1:8000/api/cases/dc_case_9a12/ \
  -H "Authorization: Bearer dev-key-12345"
```

