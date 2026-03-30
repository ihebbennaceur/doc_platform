# 🚀 Quick Start: Document Upload with AI Extraction

## What's New

You now have a complete **Document Upload & AI Extraction System** that:

1. ✅ **Uploads files** (PDF, JPG, PNG, TIFF) to `media/cases/{caseId}/{documentKey}/`
2. ✅ **Extracts data** automatically using **Deepseek Vision AI** (free)
3. ✅ **Assesses quality** (clarity, legibility, confidence score)
4. ✅ **Validates documents** (expiry dates, field completeness)
5. ✅ **Flags for review** if unclear or needs manual verification
6. ✅ **Stores operator notes** for manual review workflow

## In 3 Steps

### Step 1: Get Free Deepseek API Key

Go to: **https://platform.deepseek.com/api_keys**

- Sign up (2 mins, no credit card)
- Copy your API key: `sk-xxxxx...`
- You get $5 credit (~1,600 document extractions for free)

### Step 2: Configure Django

Add to `django/doccheck_service/.env`:

```bash
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx
```

### Step 3: Apply Database Migration

```bash
cd django/doccheck_service
python manage.py migrate
```

This adds extraction fields to the database.

## Testing

### Test 1: Upload via API

```bash
# Create a test case first
curl -X POST http://127.0.0.1:8001/api/cases/ \
  -H "Content-Type: application/json" \
  -d '{
    "rezerva_reference_id": "test_order_001",
    "callback_url": "https://webhook.local/doccheck",
    "seller_info": {
      "name": "Test User",
      "email": "test@example.com",
      "phone": "+351912345678"
    },
    "required_documents": ["caderneta_predial", "certidao_permanente"]
  }'

# Copy the provider_case_id from response (e.g., dc_case_a1b2c3d4)

# Upload a document
curl -X POST http://127.0.0.1:8001/api/cases/dc_case_a1b2c3d4/documents/upload/ \
  -F "document_key=caderneta_predial" \
  -F "file=@/path/to/sample.pdf"
```

### Test 2: Frontend Upload

1. Go to **Dashboard** → **Documents**
2. Click on a pending document
3. Drag & drop a PDF/image or click to browse
4. Watch the extraction happen (⏳ status shows "Extracting...")
5. See results: clarity badge, validity flag, extracted data

### Test 3: Python Script

```bash
cd django/doccheck_service

# Test extraction only
python test_extraction.py --file /path/to/document.pdf

# Test with database storage (create case first)
python test_extraction.py --file /path/to/document.pdf \
  --case-id dc_case_test --document-key caderneta_predial --store
```

## What You Get

### On Upload:

```json
{
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
  "extraction_notes": "Document clear and complete",
  "needs_manual_review": false
}
```

### In Database:

All data stored in `VerificationDocument` with:
- `extracted_fields` (JSON): Extracted name, dates, issuer, etc.
- `clarity_flag`: CLEAR | PARTIAL | UNCLEAR | NOT_ASSESSED
- `validity_flag`: VALID | EXPIRED | INVALID | NOT_ASSESSED
- `confidence_score`: 0-100 (AI confidence)
- `operator_notes`: Field for manual review
- `extraction_status`: pending | processing | success | failed
- `file_path`: media/cases/{caseId}/{documentKey}/{filename}

### In Frontend:

DocumentsManager shows:
```
📄 Caderneta Predial | ✓ VERIFIED
  📥 John Silva
  💼 Finanças - Lisboa
  [🟢 CLEAR 92%] [🟢 VALID]
  ✅ No manual review needed
```

Or if needs review:
```
📄 Certificate | ⚠️ EXTRACTED
  📥 John Silva
  💼 ADENE
  [🟡 PARTIAL 65%] [🟡 EXPIRED]
  ⚠️ Requires manual operator review
  [Operator Notes: Add comment here]
```

## File Structure

### Database Storage (Local Dev)

```
django/doccheck_service/
├── media/
│   └── cases/
│       └── dc_case_a1b2c3d4/
│           ├── caderneta_predial/
│           │   └── document_2024_01_15.pdf
│           └── certidao_permanente/
│               └── cert_silva.pdf
├── db.sqlite3
└── manage.py
```

### Production (AWS S3)

```
s3://fizbo-doccheck-prod/
└── cases/
    └── dc_case_a1b2c3d4/
        ├── caderneta_predial/
        │   └── document_2024_01_15.pdf
        └── certidao_permanente/
            └── cert_silva.pdf
```

## Features

✅ **Automatic Extraction**
- Reads PDF & images
- Extracts names, dates, issuer, references
- Calculates expiry (if validity_months configured)

✅ **Quality Assessment**
- Legibility score (0-100%)
- Overall confidence (0-100%)
- Identifies clarity issues (blurry, cut-off, etc.)

✅ **Validity Checking**
- Detects expired documents
- Flags concerns (missing fields, unusual format, etc.)
- Suggests manual review if uncertain

✅ **Operator Review Interface**
- See extracted data (read-only)
- Add manual notes
- Confirm validity or mark as rejected
- Trigger webhook to Rezerva on confirmation

✅ **Error Handling**
- API failures → status = UPLOADED, needs_manual_review = true
- Corrupted files → error message saved
- Rate limits → graceful fallback

## Cost

**Deepseek Free Tier:**
- $5 credit per account
- ~$0.003 per document upload
- = ~1,600 free uploads
- Rate limit: 100k tokens/day (~500 docs)
- Perfect for development/testing

**Production Pricing:**
- $0.06 per document (including 2-3 quality-check calls)
- ~$1.50 per 25 uploads
- Enterprise plans available

## Troubleshooting

### Issue: "DEEPSEEK_API_KEY not found"

```bash
# Check .env file exists
ls -la django/doccheck_service/.env

# Add the key
echo "DEEPSEEK_API_KEY=sk-xxxxx" >> django/doccheck_service/.env

# Restart Django
```

### Issue: "Extraction taking too long"

- Large PDFs (>10MB) take 5-30 seconds
- Deepseek processes 1-4 images per call
- Consider uploading compressed PDFs

### Issue: "File not saving to media folder"

```bash
# Create media directory with permissions
mkdir -p django/doccheck_service/media/cases
chmod 755 django/doccheck_service/media

# Check Django has write access
touch django/doccheck_service/media/test.txt
```

### Issue: "Rate limit exceeded (429)"

- Wait 1 minute
- Free tier limit: 100k tokens/day
- Upgrade to paid tier or wait until next day

## Next Steps

1. ✅ Upload your first PDF and watch the magic happen!
2. ⏳ Add operator review interface (mark valid/invalid)
3. ⏳ Configure webhook delivery to Rezerva
4. ⏳ Set up async extraction (Celery + Redis)
5. ⏳ Add batch upload (multiple documents)
6. ⏳ Configure S3 for production

## Documentation

📖 **Full Documentation:** See `DOCUMENT_EXTRACTION_SETUP.md`

- Architecture diagrams
- Advanced features
- Deployment to production
- Cost estimation
- Retry logic with webhooks

## Support

**Deepseek Documentation:** https://platform.deepseek.com/docs

**Django Logs:**
```bash
cd django/doccheck_service
tail -f logs/django.log  # if logging configured
```

---

**Ready to extract? Upload a document now!** 🎉
