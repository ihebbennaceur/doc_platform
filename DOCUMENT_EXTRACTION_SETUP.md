# Document Extraction & AI Validation System

## Overview

This system provides automated document upload, storage, and AI-powered extraction for property verification documents. Documents are uploaded to the Django backend, stored locally (or S3 in production), and analyzed using **Deepseek AI Vision** to extract:

- **Names & Identifiers**: Person/entity name, reference numbers, property IDs
- **Dates**: Issue date, expiry date, validity calculation
- **Issuer Information**: Who issued the document
- **Clarity Assessment**: Document legibility, confidence score (0-100)
- **Validity Assessment**: Is the document expired, valid, or invalid
- **Manual Review Flags**: Operator review needed for unclear/incomplete documents

## Architecture

```
Frontend (Next.js)
    ↓
    └─→ POST /api/cases/{caseId}/documents/upload/
                ↓
        Django Backend (Port 8001)
                ↓
        1. Save file to media/cases/{caseId}/{documentKey}/
        2. Mark status: "processing"
                ↓
        ExtractionService
                ↓
        3. Read file from disk
        4. Encode to Base64
        5. Send to Deepseek Vision API
                ↓
        6. Parse JSON response
        7. Extract fields:
            - extracted_fields (name, dates, issuer, etc.)
            - clarity_assessment (legibility, confidence)
            - validity_assessment (expiry, validity concerns)
                ↓
        8. Update Document model with results:
            - status → EXTRACTED (if needs review) or VERIFIED (if valid)
            - extracted_fields, clarity_flag, validity_flag, confidence_score
            - operator_notes (ready for manual review)
                ↓
        9. Return JSON response with all extraction data
                ↓
Frontend (React)
    ↓
    └─→ Display extraction results:
        - AI confidence badge
        - Clarity flag (CLEAR/PARTIAL/UNCLEAR)
        - Validity flag (VALID/EXPIRED/INVALID)
        - Extracted data preview
        - Manual review flag with orange badge
        - Operator notes area (editable by agents)
```

## Setup Instructions

### 1. Get Deepseek API Key (Free)

Deepseek offers a **free tier with $5 credit** for testing. No credit card required.

**Steps:**
1. Go to [https://platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
2. Sign up with email
3. Verify email
4. Navigate to **API Keys** section
5. Click **Create** → copy the key
6. You get $5 credit (~1,000 API calls for document extraction)

### 2. Configure Django

**Add to `.env` file in `django/doccheck_service/`:**

```bash
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx_your_actual_key_xxxxx
```

**Verify settings in `doccheck_service/settings.py`:**

```python
# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Ensure media directory exists
os.makedirs(MEDIA_ROOT, exist_ok=True)
```

### 3. Run Migrations

```bash
cd django/doccheck_service
python manage.py makemigrations
python manage.py migrate
```

This creates/updates these database tables:
- `VerificationDocument` (enhanced with extraction fields)
- `VerificationCase` (unchanged)
- `DocumentValidity` (reference table)
- `WebhookEvent` (for retry logic)

### 4. Test the System

**Upload a test PDF/image:**

```bash
curl -X POST http://127.0.0.1:8001/api/cases/dc_case_test123/documents/upload/ \
  -F "document_key=caderneta_predial" \
  -F "file=@/path/to/sample.pdf"
```

**Expected Response:**

```json
{
  "document_key": "caderneta_predial",
  "status": "extracted",
  "extraction_status": "success",
  "extracted_fields": {
    "name": "João Silva",
    "date_issued": "2023-01-15",
    "date_expiry": "2033-01-15",
    "issuer": "Finanças - Lisboa",
    "reference_number": "0000123456"
  },
  "clarity_flag": "CLEAR",
  "validity_flag": "VALID",
  "confidence_score": 92,
  "extraction_notes": "Document clearly visible, all required fields present",
  "needs_manual_review": false,
  "all_fields_present": true
}
```

## Frontend Integration

### Using DocumentsManagerEnhanced Component

Replace old DocumentsManager with enhanced version:

```tsx
import { DocumentsManagerEnhanced as DocumentsManager } from '@/components/DocumentsManagerEnhanced';

<DocumentsManager 
  userRole={userRole}
  documents={documents}
  onUpload={handleDocumentUpload}
/>
```

### Displaying Extraction Results

The component automatically shows:

- **Extraction Status Indicator**:
  - ⏳ Processing (spinning animation while AI extracts)
  - ✅ Success with extracted data preview
  - ❌ Failed with error message

- **Clarity Badge**: `CLEAR (92%)` / `PARTIAL (65%)` / `UNCLEAR (40%)`

- **Validity Badge**: `VALID` / `EXPIRED` / `INVALID` / `NOT_ASSESSED`

- **Extracted Data Preview**: Name, issuer, dates

- **Manual Review Alert**: Orange `⚠️ Requires Manual Review` badge if AI is uncertain

- **Operator Notes Section**: For agents to add comments

## Model Fields Reference

### VerificationDocument

```python
# Extraction Results
extracted_fields: JSONField
    {
        "name": "João Silva",
        "date_issued": "2023-01-15",
        "date_expiry": "2033-01-15",
        "issuer": "Finanças",
        "reference_number": "0000123456",
        "property_reference": "PT001234"
    }

clarity_flag: ChoiceField
    Options: CLEAR | PARTIAL | UNCLEAR | NOT_ASSESSED

clarity_assessment: JSONField
    {
        "is_clear": true,
        "legibility": 95,
        "overall_confidence": 92,
        "issues": []
    }

validity_flag: ChoiceField
    Options: VALID | EXPIRED | INVALID | NOT_ASSESSED

validity_assessment: JSONField
    {
        "is_valid": true,
        "is_expired": false,
        "validity_period_months": 120,
        "concerns": []
    }

confidence_score: IntegerField
    Range: 0-100 (overall AI confidence)

needs_manual_review: BooleanField
    true if clarity < 70% or validity uncertain

operator_notes: TextField
    Manual notes from agent/operator review

extraction_notes: TextField
    AI observations (read-only)

extraction_status: CharField
    Options: pending | processing | success | failed
```

## Cost Estimation

**Deepseek Pricing** (as of March 2026):

- Vision API: ~$0.003 per image (1-4 images per call)
- Free tier: $5 credit = ~1,600 document extractions
- Production: ~$0.06 per document upload (2-3 calls per doc for high-quality extraction)

**Daily Limits (Free):**
- Requests: 100,000 tokens/day (sufficient for ~500 document uploads)
- Concurrent: 10 requests/second

## Error Handling

### If Deepseek API Fails

```python
# Extraction failed → status = UPLOADED, needs_manual_review = True
# extraction_status = 'failed'
# extraction_error = 'Deepseek API error: 429 - Rate limit exceeded'

# Frontend shows: ❌ Extraction failed - Manual review required
```

### If File is Corrupted

```python
# extraction_error = 'Failed to read file: PDF is corrupted'
# status = UPLOADED
```

### If Response Format is Invalid

```python
# extraction_error = 'Failed to parse AI response as JSON'
# Operator must manually enter data
```

## Advanced Features

### 1. Retry Logic (Webhook Delivery)

If operator confirms document as `VERIFIED`, the system can send webhook to Rezerva:

```python
# models.py - WebhookEvent
class WebhookEvent(models.Model):
    provider_case = ForeignKey(VerificationCase)
    payload_json = JSONField()
    delivery_status = CharField()  # pending, success, failed
    attempt_count = IntegerField()  # up to 3 retries
    last_attempt_at = DateTimeField()
```

### 2. OCR Data Extraction

For scanned PDFs, Deepseek Vision can extract:

```json
{
  "extracted_fields": {
    "date_issued": "2023-01-15",  // from OCR
    "issuer": "Câmara Municipal de Lisboa",  // from OCR
    "property_ref": "0000123456"  // from OCR
  }
}
```

### 3. Manual Review Interface

**For Operators/Agents:**

- See extracted data (read-only)
- See AI assessment (clarity, validity, confidence)
- Add manual notes: `"Signature matches ID on file. Approved."`
- Confirm validity: `status = VERIFIED` or `status = REJECTED`
- Trigger webhook to Rezerva on confirmation

## Deployment Notes

### Development (Local)

```bash
# Files stored in: django/doccheck_service/media/cases/{caseId}/{documentKey}/
# Example: media/cases/dc_case_a1b2c3d4/caderneta_predial/document.pdf
```

### Production (AWS S3)

Configure in `settings.py`:

```python
# Use django-storages + boto3
INSTALLED_APPS += ['storages']

AWS_STORAGE_BUCKET_NAME = 'fizbo-doccheck-prod'
AWS_S3_REGION_NAME = 'eu-west-1'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Files stored in: s3://fizbo-doccheck-prod/cases/{caseId}/{documentKey}/
```

## Troubleshooting

### Issue: "Deepseek API Key not found"

**Solution:**
```bash
# Check .env file exists in django/doccheck_service/
cat django/doccheck_service/.env | grep DEEPSEEK

# If empty, add:
echo "DEEPSEEK_API_KEY=sk-xxxxx" >> django/doccheck_service/.env

# Restart Django server
```

### Issue: "Rate limit exceeded" (429 error)

**Solution:**
- Wait 1 minute before retrying
- Free tier has 100k tokens/day (~500 documents)
- Upgrade to paid tier or wait until next day

### Issue: Extraction taking > 30 seconds

**Solution:**
- Large PDF files (>10MB) take longer
- Consider async extraction with Celery (future enhancement)
- Split large PDFs into multiple pages

### Issue: Document file not saving

**Solution:**
```bash
# Ensure media directory exists and has write permissions
mkdir -p django/doccheck_service/media/cases
chmod 755 django/doccheck_service/media

# Check Django logs for permission errors
```

## Next Steps

1. ✅ Upload test PDF → verify extraction works
2. ⏳ Implement operator review interface (UI for adding notes)
3. ⏳ Implement webhook delivery to Rezerva (status updates)
4. ⏳ Add document comparison (before/after valid dates)
5. ⏳ Add batch extraction (upload multiple documents)
6. ⏳ Implement async extraction with Celery + Redis

## Support

**For Deepseek API issues:**
- Docs: https://platform.deepseek.com/docs
- Support: support@deepseek.com

**For Django extraction service issues:**
- Check Django logs: `django/doccheck_service/logs/`
- Check extraction_service.py for [ExtractionService] log messages
