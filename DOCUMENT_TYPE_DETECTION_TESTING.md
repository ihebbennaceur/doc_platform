# Document Type Detection - Testing Guide

## 🧪 Quick Test Steps

### 1. Apply Migrations
```powershell
cd c:\Users\send6\Desktop\pfe_seller_platform\django\doccheck_service
python manage.py migrate
```

### 2. Start Backend
```powershell
python manage.py runserver 0.0.0.0:8000
```

### 3. Test Extraction with Type Detection

#### Using cURL
```bash
# Create a case first
curl -X POST http://localhost:8000/api/cases/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "rezerva_reference_id": "TEST-001",
    "seller": {
      "full_name": "Test Seller",
      "email": "test@example.com"
    },
    "required_documents": ["caderneta_predial"],
    "callback_url": "http://localhost:3000/webhook"
  }'

# Upload document with type selection
curl -X POST http://localhost:8000/api/cases/TEST-001/upload/caderneta_predial/ \
  -F "document_type=caderneta_predial" \
  -F "file=@/path/to/test_document.pdf"
```

#### Using Python
```python
import requests
import json

# Create case
case_response = requests.post(
    'http://localhost:8000/api/cases/create/',
    json={
        'rezerva_reference_id': 'TEST-002',
        'seller': {
            'full_name': 'Test Seller',
            'email': 'test@example.com'
        },
        'required_documents': ['caderneta_predial']
    }
)
case_id = case_response.json()['provider_case_id']

# Upload document
with open('test_document.pdf', 'rb') as f:
    files = {'file': f}
    data = {
        'document_key': 'caderneta_predial',
        'document_type': 'caderneta_predial'  # User's selection
    }
    response = requests.post(
        f'http://localhost:8000/api/cases/{case_id}/upload/caderneta_predial/',
        files=files,
        data=data
    )
    
print(json.dumps(response.json(), indent=2))
```

### 4. Verify Response Fields

Expected response should include:
```json
{
  "user_submitted_document_type": "caderneta_predial",
  "detected_document_type": "caderneta_predial",
  "document_type_confidence": 90-100,
  "document_type_match": true,
  "field_completeness": {
    "total_expected_fields": 9,
    "fields_found": 6-9,
    "missing_fields": [],
    "percentage_complete": 85-100
  },
  "fields_complete_percentage": 85-100,
  "agent_review_required": false,
  "agent_review_reason": null
}
```

### 5. Test Type Mismatch Scenario

Upload with wrong type:
```bash
curl -X POST http://localhost:8000/api/cases/{case_id}/upload/document_key/ \
  -F "document_type=certidao_permanente" \  # Wrong type
  -F "file=@/path/to/caderneta_document.pdf"  # But actual content is caderneta
```

Expected result:
```json
{
  "document_type_match": false,
  "document_type_mismatch_reason": "Mismatch: AI detected caderneta_predial but user selected certidao_permanente",
  "agent_review_required": true,
  "agent_review_reason": "Type mismatch: detected caderneta_predial but user selected certidao_permanente"
}
```

### 6. Test Incomplete Document Scenario

Upload partial/unclear document:
```bash
curl -X POST http://localhost:8000/api/cases/{case_id}/upload/document_key/ \
  -F "document_type=caderneta_predial" \
  -F "file=@/path/to/partial_document.jpg"  # Partial image
```

Expected result:
```json
{
  "fields_complete_percentage": 45,
  "missing_fields": ["nif", "date_expiry", "property_reference", "condominium", "unit_number"],
  "agent_review_required": true,
  "agent_review_reason": "Incomplete fields: 4/9 (45% complete)"
}
```

---

## 🧬 Test Cases

### Test Case 1: Perfect Match, Complete Data
**Setup:** Upload clear caderneta_predial with all fields visible
**Expected:**
- ✅ document_type_match = true
- ✅ fields_complete_percentage = 100
- ✅ agent_review_required = false
- ✅ status = "verified"

### Test Case 2: Type Mismatch
**Setup:** Upload caderneta but select certidao in form
**Expected:**
- ❌ document_type_match = false
- ✅ agent_review_required = true
- ✅ agent_review_reason contains "Type mismatch"

### Test Case 3: Incomplete Fields
**Setup:** Upload document with only 60% of fields visible
**Expected:**
- ✅ fields_complete_percentage = 60
- ✅ missing_fields = ["nif", "property_reference", "condominium"]
- ✅ agent_review_required = true
- ✅ agent_review_reason contains "Incomplete fields"

### Test Case 4: Low Clarity
**Setup:** Upload very faint or damaged document
**Expected:**
- ✅ clarity_flag = "UNCLEAR"
- ✅ clarity.overall_confidence < 70
- ✅ agent_review_required = true
- ✅ agent_review_reason contains "Low clarity"

### Test Case 5: Expired Document
**Setup:** Upload document past expiry date
**Expected:**
- ✅ is_expired = true
- ✅ validity_flag = "EXPIRED"
- ✅ agent_review_required = true

---

## 📊 Monitoring Agent Review Flags

### Database Query
```python
# See documents flagged for review
from django.doccheck_service.cases.models import VerificationDocument

review_flagged = VerificationDocument.objects.filter(agent_review_required=True)
for doc in review_flagged:
    print(f"Doc: {doc.document_key}")
    print(f"  Reason: {doc.agent_review_reason}")
    print(f"  Type Match: {doc.document_type_match}")
    print(f"  Completeness: {doc.fields_complete_percentage}%")
    print(f"  Clarity: {doc.clarity_flag}")
```

### API Query
```bash
# Get all documents flagged for review (future: admin dashboard)
curl http://localhost:8000/api/cases/{case_id}/
```

---

## 🐛 Debugging

### Check Extraction Service Logs
```python
# In extraction_service.py, logs show:
# [ExtractionService] Starting extraction for /path/to/file
# [ExtractionService] File media type: application/pdf
# [ExtractionService] Calling Deepseek API...
# [ExtractionService] Deepseek API response: {...}
```

### View Database Fields
```python
from django.doccheck_service.cases.models import VerificationDocument

doc = VerificationDocument.objects.first()
print(f"Detected Type: {doc.detected_document_type}")
print(f"Type Confidence: {doc.document_type_confidence}")
print(f"Type Match: {doc.document_type_match}")
print(f"Field Completeness: {doc.field_completeness}")
print(f"Fields Complete %: {doc.fields_complete_percentage}")
print(f"Missing Fields: {doc.missing_fields}")
print(f"Agent Review Required: {doc.agent_review_required}")
print(f"Agent Review Reason: {doc.agent_review_reason}")
```

### Frontend Console
```javascript
// In browser console, watch extraction updates
console.log('Document extraction result:', selectedDoc);
console.log('Type match:', selectedDoc.document_type_match);
console.log('Completeness:', selectedDoc.fields_complete_percentage);
console.log('Review required:', selectedDoc.agent_review_required);
```

---

## ✅ Validation Checklist

- [ ] Migration runs successfully: `python manage.py migrate`
- [ ] Backend starts without errors
- [ ] Can create cases: POST `/api/cases/create/`
- [ ] Can upload documents: POST `/api/cases/{id}/upload/{key}/`
- [ ] Response includes `detected_document_type`
- [ ] Response includes `document_type_confidence`
- [ ] Response includes `document_type_match`
- [ ] Response includes `field_completeness` object
- [ ] Response includes `fields_complete_percentage`
- [ ] Response includes `missing_fields` array
- [ ] Response includes `agent_review_required` boolean
- [ ] Response includes `agent_review_reason` string
- [ ] Type mismatch triggers `agent_review_required = true`
- [ ] Low completeness (< 80%) triggers review flag
- [ ] Frontend shows type detection section
- [ ] Frontend shows field completeness progress bar
- [ ] Frontend shows agent review banner when flagged
- [ ] Type mismatch shows orange border
- [ ] Complete fields show green progress bar
- [ ] Incomplete fields show red progress bar
- [ ] Missing fields listed in UI

---

## 🚀 Production Deployment

1. **Backup Database**
   ```bash
   # PostgreSQL
   pg_dump -U postgres doccheck_db > backup_pre_deploy.sql
   ```

2. **Apply Migrations**
   ```bash
   python manage.py migrate cases 0003_add_document_type_detection
   ```

3. **Test in Production-Like Environment**
   ```bash
   # Run test suite
   python manage.py test cases
   ```

4. **Monitor Agent Review Flags**
   - Check dashboard for newly flagged documents
   - Verify AI detections are accurate
   - Adjust confidence thresholds if needed

5. **Rollback Plan** (if needed)
   ```bash
   python manage.py migrate cases 0002_add_ai_extraction
   ```

---

**Last Updated:** 2025-01-01
**Status:** Ready for Testing ✅
