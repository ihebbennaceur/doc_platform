# DocCheck Workflow Implementation Briefing

**Date:** March 27, 2026  
**Status:** Phase 1 (P0) – Free Assessment + Document Upload  
**Scope:** Q&A flow → case creation → document collection → validation

---

## Table of Contents

1. [Overview](#overview)
2. [Document Validity Rules (Section 5.1)](#document-validity-rules)
3. [Architecture: Microservice + Frontend](#architecture)
4. [Workflow: Step-by-Step](#workflow)
5. [Backend Implementation](#backend-implementation)
6. [Frontend Implementation](#frontend-implementation)
7. [API Contract](#api-contract)
8. [Deployment & Testing](#deployment--testing)

---

## Overview

The DocCheck tool enables sellers to:

1. **Answer 12 diagnostic questions** (Q1-Q12) to assess their property profile
2. **Receive a persona classification** (Urban Resident, Non-Resident, Heir, Divorce, Rural)
3. **Learn which documents are missing** from their profile
4. **Upload documents** to validate against stated requirements
5. **Track document expiry** across the 7-year sales timeline

**Key Constraint:** After Q&A completes, the seller enters a **case** where they upload missing documents for verification. The backend validates document types, checks expiry dates, and tracks OCR extraction if applicable.

---

## Document Validity Rules

### Section 5.1: Document Reference Table

| Document | Validity | Obtainable By | Cost | Notes |
|---|---|---|---|---|
| **Caderneta Predial Urbana** | 12 months | Owner only | €0 (online) / €1 (in-person) | Free assessment identifies if expired; seller must renew |
| **Certidão Permanente** | 6 months | Anyone | €15 (online) / €20 (in-person) | Valid for transaction; short window; high priority |
| **Licença de Utilização** | No expiry | Procuração simples | €6–€60 (varies by Câmara) | May not exist for pre-1951 buildings; required for post-1951 |
| **Certificado Energético** | 10 years | Perito Qualificado (ADENE) | €150–€300 all-in | Most expensive; required by law; triggers risk flag if absent/low rating (F/G) |
| **Declaração do Condomínio** | ~30 days | No authorization needed | €0–€50 | Only for condominiums; short validity; must request from admin |
| **Distrate de Hipoteca** | At escritura (final deed) | Seller + bank | €0 (bank) + €50 (registration) | Only if mortgaged; bank provides; seller must submit |
| **Habilitação de Herdeiros** | Permanent | Procuração com poderes especiais | €150–€425 (Balcão das Heranças) | Only for inheritance; legal proof of heir status; complex |

### DocCheck Validity Logic

**Assessment Phase (Q&A):**
- Based on answers (property type, age, mortgage, ownership), DocCheck calculates **always-required** documents.
- Always Required: `caderneta_predial` + `certidao_permanente` (€15–€21 total).
- Additional docs depend on persona and property profile (see below).

**Case Phase (Upload):**
- Seller uploads documents one by one.
- Backend extracts file metadata (upload timestamp, mime type, file size).
- If OCR enabled: extract text, detect document type, validate key fields (dates, issuer, etc.).
- Flag if document is **expired** (comparison: upload_date – doc_validity_months > doc_issue_date).
- Flag if document type **mismatch** (e.g., uploaded "Certificado Energético" but backend expected "Caderneta").

### Validity Rules by Persona & Property

**P1 – Urban Resident** (PT resident, city apartment, mortgage):
- Always: Caderneta + Certidão
- If mortgaged: + Distrate
- If post-1951: + Licença
- If post-2007: + Ficha Técnica Habitação
- If no valid energy cert: + Certificado Energético
- If condominium: + Declaração Condomínio
- **Typical cost:** €165–€350 (energy cert dominates)

**P2 – Non-Resident** (EU/non-EU, abroad):
- All P1 docs PLUS
- + Habilitação (to prove ownership abroad)
- + Power of Attorney (POA) for fiscal rep
- **Typical cost:** €315–€775 (add POA + potential legal)

**P3 – Heir** (inheritance, multiple heirs):
- All P1 docs PLUS
- + Habilitação de Herdeiros (multiple heirs need legal proof)
- + Court decree or notarized heir certification
- **Typical cost:** €315–€500 (legal complexity)

**P4 – Divorce** (joint ownership, urgent):
- All P1 docs PLUS
- + Court divorce decree
- + Division of assets agreement
- + Both spouses' signatures on Certidão
- **Typical cost:** €165–€350 (urgent timeline → express tier)

**P5 – Rural/Legacy** (quinta, pre-1951, elderly):
- All docs (may be missing or irregular)
- + Licença (often missing for old properties)
- + Regularization paperwork (if needed)
- + Notarized statements (for missing docs)
- **Typical cost:** €300–€500+ (custom quote; heritage tier)

---

## Architecture

### Microservice Split

**Old:** Monolith backend (`backend_django/backend_seller_platform/modules/doccheck/`)
- Legacy code remains as-is for now (backward compatibility).

**New:** Standalone microservice (`django/doccheck_service/`)
- Django 5 + DRF
- SQLite (development) / PostgreSQL (production)
- Hosted independently (e.g., separate EC2, Docker container).
- API-first design: Endpoints for assessment, case creation, document upload, webhook delivery.

**Frontend:** Next.js app (`frontend_seller_platform/`)
- Calls new microservice at `http://127.0.0.1:8001/api/` (dev) or `https://doccheck-api.fizbo.pt/api/` (prod).
- Q&A form → assessment result → case creation → document upload UI.

### Service Boundary

```
┌─ Frontend (Next.js) ─────┐
│  /doccheck (Q&A UI)      │
│  /dashboard (case tracker)
└───────────┬──────────────┘
            │ HTTP/JSON
            ↓
┌─ DocCheck Microservice ──┐
│  POST /api/cases/ (Q&A)  │
│  GET /api/cases/{id}/    │
│  PATCH /api/cases/{id}/status/
│  POST /api/cases/{id}/documents/upload
│  GET /api/schema/swagger/ (docs)
└──────────────────────────┘
```

---

## Workflow

### Phase 1: Assessment (Q&A Questions 1–12)

**Frontend UI:**
- 12-question form with conditional rendering (some Q skip based on answers).
- Progress bar (step N/12).
- Answers stored locally (localStorage) for resume capability.
- On final submit → POST to microservice.

**Questions:**

1. **Email** (required): Seller's email for case tracking.
2. **Property Type**: apartment, house, land, other → triggers doc rules.
3. **Condominium?** (yes/no) → Adds "Declaração Condomínio".
4. **Building Age**: pre_1951, 1951–1990, 1991–2007, post_2007 → triggers energy cert, ficha técnica rules.
5. **Mortgaged?** (yes/no) → Adds "Distrate de Hipoteca".
6. **How Acquired**: purchase, inheritance, divorce, gift, other → Persona detection; adds Habilitação if inheritance.
7. **Primary Residence?** (yes/no) → Non-resident flag.
8. **All Owners Available?**: yes, one_abroad, one_deceased, disputed → Risk flag.
9. **Energy Certificate Valid?** (yes/no) → Adds if no.
10. **Seller Residency**: portugal_resident, non_resident_eu, non_resident_other → **P1 vs P2 persona**.
11. **Number of Heirs** (if inheritance): 1, 2–3, 4+, disputed → **P3 (heir) persona**.
12. **Divorce Case?** (if divorce acquisition) → **P4 (divorce) persona**.
13. **Urgency**: flexible, 3_months, 1_month, urgent → Tier override (urgent → express €1,499).

### Phase 2: Assessment Result

**Frontend Display:**
- **Persona Card**: Name + description (e.g., "Urban Resident" + "PT resident, city apartment").
- **Tier Recommendation**: Name + price + turnaround (e.g., "Standard €399 / 7 days").
- **Missing Documents List**: Formatted as warning cards with cost + issuer.
- **Risk Flags**: Severity badges (critical/high/medium/low) + recommendations (e.g., "Old property → Recommend inspection").
- **CTA Buttons**:
  - Free tier → "View SmartCMA" (redirect to CMA report).
  - Paid tier → "Proceed to Checkout" (redirect to /orders/create).

**Backend Returns (JSON):**
```json
{
  "email": "seller@example.com",
  "persona": {
    "slug": "urban_resident",
    "name": "Urban Resident",
    "description": "PT resident, city apartment, mortgage"
  },
  "missing_documents": ["caderneta_predial", "certidao_permanente", "certificado_energetico"],
  "missing_document_count": 3,
  "recommended_tier": {
    "slug": "standard",
    "name": "Standard",
    "price": 399
  },
  "risk_flags": [
    {
      "key": "low_energy_rating",
      "message": "Energy class F – may affect buyer financing",
      "recommendation": "Recommend Energy Certificate update",
      "severity": "medium"
    }
  ],
  "has_risk_flags": true,
  "summary": {
    "documents_always_required": 2,
    "documents_missing_count": 3,
    "risk_flag_count": 1,
    "is_free_tier": false,
    "is_urgent": false
  }
}
```

### Phase 3: Case Creation & Document Upload

**After Assessment → Order Created (if paid tier):**

1. **Stripe Checkout** (DocReady module):
   - User selects tier (Standard €399, Premium €899, Express €1,499).
   - Stripe processes payment.
   - Webhook: `order_payment_confirmed` → Inngest workflow.

2. **Inngest Workflow** (DocReady module):
   - Create case in DocCheck microservice: `POST /api/cases/` with seller + required docs.
   - Backend returns `provider_case_id` (e.g., `dc_case_a1b2c3d4`) + `upload_token` + `upload_url`.
   - Generate upload credentials + pre-signed URLs (if S3).
   - Email seller: "Your documents are ready to upload. [Upload Link]"

3. **Document Upload UI** (Seller Dashboard module):
   - For each missing document:
     - Display doc info: name, validity, cost, issuer.
     - File input (drag-drop or click).
     - On select → `POST /api/cases/{provider_case_id}/documents/upload` with file + doc_key.
   - Backend:
     - Validates MIME type (PDF/image only).
     - Stores file in S3 or local storage.
     - If OCR enabled: Extract text, detect type, validate expiry.
     - Return: `{ status: "uploaded", document_key: "caderneta_predial", extracted_date: "2025-02-15" }`.
   - Frontend updates UI: ✓ Caderneta Predial (uploaded 2025-02-15, expires 2026-02-15).

4. **Document Validation** (Backend):
   - **Expiry Check**: If `extracted_date` + `validity_months` < today → Flag as expired.
   - **Type Check**: If uploaded file name ≠ expected doc_key → Warn user to re-upload correct doc.
   - **OCR Extraction** (optional):
     - Extract issuer, date, property ref from PDF.
     - Validate against known issuers (Finanças, IRN, Câmara, etc.).
   - **Status Tracking**: Document model stores: `{ case, doc_key, status (pending/uploaded/verified/expired), file_path, extracted_data, uploaded_at }`.

---

## Backend Implementation

### Django Models (DocCheck Microservice)

#### VerificationCase (already exists, enhanced)

```python
class VerificationCase(models.Model):
    class CaseStatus(models.TextChoices):
        CREATED = 'created', 'Created'
        IN_REVIEW = 'in_review', 'In Review'
        VERIFIED = 'verified', 'Verified'
        REJECTED = 'rejected', 'Rejected'

    provider_case_id = models.CharField(primary_key=True, max_length=32)
    rezerva_reference_id = models.CharField(max_length=64, unique=True)  # from payment webhook
    callback_url = models.URLField()  # where to POST results
    status = models.CharField(max_length=20, choices=CaseStatus.choices, default=CaseStatus.CREATED)
    
    # Seller info
    seller_name = models.CharField(max_length=255)
    seller_email = models.EmailField()
    seller_phone = models.CharField(max_length=32)
    
    # Assessment result (denormalized from order)
    persona_slug = models.CharField(max_length=50, default='urban_resident')
    tier_slug = models.CharField(max_length=50, default='standard')
    required_documents = models.JSONField(default=list)  # ['caderneta_predial', 'certidao_permanente', ...]
    
    upload_token = models.CharField(max_length=64, default='', blank=True)
    expires_at = models.DateTimeField()
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### VerificationDocument (already exists, enhanced)

```python
class VerificationDocument(models.Model):
    class DocumentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending Upload'
        UPLOADED = 'uploaded', 'Uploaded'
        VERIFIED = 'verified', 'Verified'
        EXPIRED = 'expired', 'Expired'
        REJECTED = 'rejected', 'Rejected'

    provider_case = models.ForeignKey(VerificationCase, related_name='documents', on_delete=models.CASCADE)
    document_key = models.CharField(max_length=128)  # e.g., 'caderneta_predial'
    status = models.CharField(max_length=32, choices=DocumentStatus.choices, default=DocumentStatus.PENDING)
    
    file_path = models.CharField(max_length=255, blank=True)  # S3 key or local path
    file_name = models.CharField(max_length=255, blank=True)
    file_size = models.IntegerField(default=0)
    mime_type = models.CharField(max_length=50, blank=True)
    
    # Extracted data (OCR)
    extracted_data = models.JSONField(default=dict, blank=True)  # { date: '2025-01-15', issuer: 'Finanças', ... }
    extracted_date = models.DateField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    expiry_date = models.DateField(null=True, blank=True)  # calculated from extracted_date + validity_months
    
    reason = models.CharField(max_length=255, blank=True)  # e.g., 'Document expired'
    uploaded_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('provider_case', 'document_key')
```

#### DocumentValidity (new reference table)

```python
class DocumentValidity(models.Model):
    """Reference table for document types and validity rules"""
    
    document_key = models.CharField(max_length=128, unique=True, primary_key=True)
    name = models.CharField(max_length=255)  # 'Caderneta Predial Urbana'
    validity_months = models.IntegerField(null=True)  # 12, 6, 10*12, None
    cost_min = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_max = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    issuer = models.CharField(max_length=255)  # 'Finanças', 'IRN', 'ADENE', etc.
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Document Validities"
```

### API Endpoints (microservice)

#### 1. POST /api/cases/ – Create case from assessment

**Request:**
```json
{
  "rezerva_reference_id": "order_12345_abc",
  "callback_url": "https://api.example.com/webhooks/doccheck",
  "seller": {
    "full_name": "João Silva",
    "email": "joao@example.com",
    "phone": "+351912345678"
  },
  "assessment_result": {
    "persona": "urban_resident",
    "tier": "standard",
    "missing_documents": ["caderneta_predial", "certidao_permanente", "certificado_energetico"]
  }
}
```

**Response (201 Created):**
```json
{
  "provider_case_id": "dc_case_a1b2c3d4",
  "upload_url": "https://doccheck.fizbo.pt/upload/dc_case_a1b2c3d4?token=xyz",
  "status": "created",
  "expires_at": "2026-04-03T12:00:00Z",
  "documents": [
    { "document_key": "caderneta_predial", "status": "pending" },
    { "document_key": "certidao_permanente", "status": "pending" },
    { "document_key": "certificado_energetico", "status": "pending" }
  ]
}
```

#### 2. POST /api/cases/{provider_case_id}/documents/upload – Upload document

**Request:** (multipart/form-data)
```
POST /api/cases/dc_case_a1b2c3d4/documents/upload
Content-Type: multipart/form-data

document_key: caderneta_predial
file: <binary PDF/image>
```

**Response (201 Created):**
```json
{
  "document_key": "caderneta_predial",
  "status": "uploaded",
  "file_name": "caderneta_silva_jan2025.pdf",
  "file_size": 1048576,
  "extracted_data": {
    "date": "2025-01-15",
    "issuer": "Finanças - Lisboa",
    "property_ref": "0000123456"
  },
  "expiry_date": "2026-01-15",
  "is_expired": false,
  "uploaded_at": "2026-03-27T10:30:00Z"
}
```

#### 3. GET /api/cases/{provider_case_id}/ – Retrieve case + documents

**Response:**
```json
{
  "provider_case_id": "dc_case_a1b2c3d4",
  "status": "in_review",
  "seller_name": "João Silva",
  "seller_email": "joao@example.com",
  "persona": "urban_resident",
  "tier": "standard",
  "documents": [
    {
      "document_key": "caderneta_predial",
      "status": "verified",
      "expiry_date": "2026-01-15",
      "is_expired": false,
      "uploaded_at": "2026-03-27T10:30:00Z"
    },
    {
      "document_key": "certidao_permanente",
      "status": "pending",
      "expiry_date": null
    },
    {
      "document_key": "certificado_energetico",
      "status": "uploaded",
      "expiry_date": "2036-03-15",
      "is_expired": false
    }
  ],
  "created_at": "2026-03-27T08:00:00Z"
}
```

#### 4. PATCH /api/cases/{provider_case_id}/status/ – Update case status + send webhook

**Request:**
```json
{
  "status": "verified",
  "notes": "All documents verified by operator"
}
```

**Response + Webhook Delivery:**
- Updates case status to "verified".
- POSTs to `callback_url` with result: `{ provider_case_id, status, documents_verified_at, ... }`.
- Retries webhook up to 3 times if delivery fails.

---

## Frontend Implementation

### Components & Pages

#### 1. /doccheck/page.tsx – Q&A Form (existing, enhanced)

**Changes:**
- Persist answers to localStorage (already done).
- On final submit: Call microservice instead of monolith.
- On result: Display persona + tier + missing docs + CTAs.
- CTA: "Proceed to Checkout" (if paid) → `/orders/create?tier=standard&case_id=dc_case_xxx`.

**API Call:**
```typescript
const response = await fetch('http://127.0.0.1:8001/api/cases/', {
  method: 'POST',
  body: JSON.stringify({
    email: answers.email,
    property_type: answers.property_type,
    has_condominium: answers.has_condominium,
    // ... all 12 questions
  }),
});
const result = await response.json();
// result.assessment_result contains persona, tier, missing_documents
```

#### 2. /dashboard/[caseId]/page.tsx – Case Tracker (new)

**Display:**
- Case ID, seller name, created date.
- Progress bar: N/M documents uploaded.
- For each document:
  - Name + validity + cost.
  - Status badge (pending/uploaded/verified/expired).
  - File upload button (if pending).
  - Expiry countdown (if verified).

**Upload Handler:**
```typescript
const handleDocumentUpload = async (file: File, documentKey: string) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('document_key', documentKey);

  const response = await fetch(
    `http://127.0.0.1:8001/api/cases/${caseId}/documents/upload`,
    { method: 'POST', body: formData }
  );
  const result = await response.json();
  // Update UI with extracted_date, expiry_date, status
};
```

#### 3. /orders/create/page.tsx – Checkout (existing, updated)

**Changes:**
- Accept `tier` and `case_id` from query params.
- Pre-fill seller info from assessment (if available).
- On payment success: Create case in microservice + send case_id to seller.

---

## API Contract

### Microservice Endpoints (OpenAPI/Swagger)

All endpoints documented at:
- **Swagger UI:** `http://127.0.0.1:8001/api/schema/swagger/`
- **Redoc:** `http://127.0.0.1:8001/api/schema/redoc/`
- **OpenAPI JSON:** `http://127.0.0.1:8001/api/schema/`

### Authentication (Future)

- **Development:** None (open access).
- **Production:** API key + HMAC signature (per Rezerva contract).
  - Header: `X-API-Key: <api_key>`
  - Header: `X-Signature: HMAC-SHA256(payload, secret)`

### Error Handling

All errors return JSON:
```json
{
  "error": "invalid_request",
  "message": "Email already registered for this assessment",
  "status": 400
}
```

---

## Deployment & Testing

### Local Development

```bash
# Terminal 1: Start DocCheck microservice
cd django/doccheck_service
python manage.py runserver 0.0.0.0:8001

# Terminal 2: Start frontend
cd frontend_seller_platform
npm run dev  # http://localhost:3000

# Terminal 3: Start monolith (optional, for backward compat)
cd backend_django/backend_seller_platform
python manage.py runserver 0.0.0.0:8000
```

### API Testing

**Create Assessment:**
```bash
curl -X POST http://127.0.0.1:8001/api/cases/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "seller@example.com",
    "property_type": "apartment",
    "has_condominium": false,
    "building_construction": "post_2007",
    "has_mortgage": true,
    "acquisition_type": "purchase",
    "is_primary_residence": true,
    "has_valid_energy_cert": false,
    "all_owners_available": "yes",
    "seller_residency": "portugal_resident",
    "urgency": "flexible"
  }'
```

**Upload Document:**
```bash
curl -X POST http://127.0.0.1:8001/api/cases/dc_case_xxx/documents/upload \
  -F "document_key=caderneta_predial" \
  -F "file=@/path/to/caderneta.pdf"
```

### Color Palette (from shared/theme/colors.ts)

Use these colors in the UI to match Fizbo brand:

| Element | Color | Usage |
|---|---|---|
| Primary | `#2E5D4B` (Forest Green) | Buttons, headings, emphasis |
| Accent | `#4A9B7F` (Mid Green) | Links, hover states |
| Gold | `#C9A84C` | Pricing, highlights |
| Background | `#F5F0E8` (Warm Cream) | Page background |
| Text Dark | `#1A1A2E` | Body text |
| Error | `#D32F2F` | Expired docs, alerts |
| Warning | `#F57C00` | Missing docs, caution |
| Success | `#388E3C` | Verified docs |

---

## Summary: Next Steps

1. **Backend (DocCheck Microservice):**
   - ✅ Models: VerificationCase, VerificationDocument, DocumentValidity
   - ✅ Endpoints: POST /cases/, POST /documents/upload, GET /cases/{id}/
   - ⏳ OCR integration (optional Phase 2): Extract text from PDFs
   - ⏳ Webhook delivery: PATCH /status/ + outbound POST to callback_url

2. **Frontend:**
   - ⏳ Update API calls to point to microservice (instead of monolith)
   - ⏳ Add case tracker page + document upload UI
   - ⏳ Use brand colors from shared theme

3. **Integration:**
   - ⏳ Remove legacy `doccheck` module from monolith (after migration verified)
   - ⏳ Add DocReady order flow (Stripe → case creation → Inngest workflow)
   - ⏳ Operator dashboard: Review cases + approve/reject documents

---

**Questions?** Refer to this document or contact the dev team.  
**Last updated:** March 27, 2026
