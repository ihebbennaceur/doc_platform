# Document Type Detection - Quick Reference

## 🎯 What Was Built

AI automatically **detects & confirms document types**, tracks **field completeness**, and **flags missing data** for agent review.

---

## ✨ Key Features

| Feature | What It Does |
|---------|-------------|
| **Type Detection** | AI identifies document type from visual content (8 types supported) |
| **Type Confirmation** | Compares AI detection against user's selection, flags mismatches |
| **Field Completeness** | Tracks how many fields were extracted (0-100%) |
| **Missing Fields List** | Shows exactly which fields are missing |
| **Auto Review Flag** | Automatically flags documents needing agent attention |

---

## 📦 New Database Fields (10)

### Type Detection
- `user_submitted_document_type` - What user selected
- `detected_document_type` - What AI detected  
- `document_type_confidence` - AI's confidence (0-100)
- `document_type_match` - Do they match? (true/false)
- `document_type_mismatch_reason` - Why they don't match

### Field Completeness
- `field_completeness` - JSON with all metrics
- `fields_complete_percentage` - Percentage (0-100)
- `missing_fields` - List of missing field names

### Agent Review
- `agent_review_required` - Should agent review it?
- `agent_review_reason` - Why? (type mismatch, incomplete, etc.)

---

## 🚀 Quick Start

### 1. Apply Database Migration
```bash
cd django/doccheck_service
python manage.py migrate
```

### 2. Upload Document with Type
```bash
curl -X POST http://localhost:8000/api/cases/{case_id}/upload/caderneta_predial/ \
  -F "document_type=caderneta_predial" \
  -F "file=@document.pdf"
```

### 3. Check Response (has new fields!)
```json
{
  "detected_document_type": "caderneta_predial",
  "document_type_confidence": 95,
  "document_type_match": true,
  "fields_complete_percentage": 85,
  "missing_fields": ["unit_number"],
  "agent_review_required": false,
  "agent_review_reason": null
}
```

---

## 🧠 How AI Validation Works

```
Upload Document
       ↓
AI Detects Type → "caderneta_predial"
       ↓
Compare with User Selection → "caderneta_predial"
       ↓
Match? YES ✓
       ↓
Extract Fields → 8/9 found
       ↓
Calculate Completeness → 88% complete
       ↓
Check Clarity → 92% clear
       ↓
Check Validity → Not expired ✓
       ↓
All Checks Pass? → agent_review_required = FALSE
       ↓
Status → VERIFIED ✓
```

---

## 🚨 When Does Agent Review Get Triggered?

| Condition | Review Flag |
|-----------|------------|
| Type mismatch (detected ≠ user) | ✅ YES |
| Missing fields (< 80% complete) | ✅ YES |
| Low clarity (< 70% confidence) | ✅ YES |
| Document expired | ✅ YES |
| All good ✓ | ❌ NO |

---

## 📊 Field Completeness Examples

```
Complete Document:
  9/9 fields found = 100% → ✅ Green bar → ✅ No review needed

Mostly Complete:
  8/9 fields found = 88% → ✅ Green bar → ✅ No review needed

Somewhat Complete:
  6/9 fields found = 67% → 🟠 Orange bar → 🚨 Review needed

Incomplete:
  3/9 fields found = 33% → 🔴 Red bar → 🚨 Review needed
```

---

## 🎨 Frontend Display

### Type Detection Box (If AI found type)
```
┌─────────────────────────────────────┐
│ 🟢 Document Type: caderneta_predial │
│    (95% confidence)                 │
│ User Selected: caderneta_predial    │
│ ✓ Types match!                      │
└─────────────────────────────────────┘
```

### Type Mismatch Box (If types don't match)
```
┌─────────────────────────────────────┐
│ 🟠 Document Type: caderneta_predial │
│ User Selected: certidao_permanente  │
│ ⚠️ Type mismatch!                   │
└─────────────────────────────────────┘
```

### Completeness Progress (Always shown)
```
Fields Extracted: 8/9 (88%)
[████████░] 88%
```

### Agent Review Banner (When needed)
```
┌─────────────────────────────────────┐
│ 🚨 Agent Review Required            │
│ Incomplete fields: 6/9 (67%)        │
└─────────────────────────────────────┘
```

---

## 📋 Files Changed

| File | Change | Type |
|------|--------|------|
| `models.py` | Added 10 fields | Modified |
| `extraction_service.py` | Enhanced prompt + logic | Modified |
| `views.py` | Store detection results | Modified |
| `serializers.py` | Return new fields | Modified |
| `0003_add_...migration.py` | Database schema | Created |
| `DocumentsManagerEnhanced.tsx` | Show type/completeness | Modified |

---

## 🧪 Test It Now

### Scenario 1: Perfect Match, Complete
```bash
# Upload document that matches user selection, all fields visible
Expected: agent_review_required = false, fields = 100%
```

### Scenario 2: Type Mismatch
```bash
# Upload caderneta but select certidao in form
Expected: agent_review_required = true, reason = "Type mismatch"
```

### Scenario 3: Incomplete Fields
```bash
# Upload document with only 60% of fields visible
Expected: agent_review_required = true, reason = "Incomplete: 5/9"
```

---

## 💡 Key Metrics

| Metric | What It Means | Example |
|--------|---------------|---------|
| `document_type_confidence` | How sure AI is about type | 95 = very sure |
| `fields_complete_percentage` | How much data was found | 88 = 8 out of 9 fields |
| `document_type_match` | Does AI agree with user? | true = yes |
| `agent_review_required` | Does agent need to check? | true = yes, review needed |

---

## 🎓 Expected Document Types

1. **caderneta_predial** - Urban property registry
2. **certidao_permanente** - Land registry certificate
3. **certificado_energetico** - Energy certificate
4. **licenca_utilizacao** - Usage license
5. **ficha_tecnica_habitacao** - Housing technical file
6. **declaracao_condominio** - Condominium declaration
7. **distrate_hipoteca** - Mortgage discharge
8. **habilitacao_herdeiros** - Heirs qualification

---

## 📱 API Endpoint

```
POST /api/cases/{case_id}/upload/{document_key}/

Parameters:
  - file (PDF or image)
  - document_type (user's selection, optional)
  - document_key (doc identifier)

Response includes:
  ✓ detected_document_type
  ✓ document_type_confidence
  ✓ document_type_match
  ✓ field_completeness
  ✓ fields_complete_percentage
  ✓ missing_fields
  ✓ agent_review_required
  ✓ agent_review_reason
```

---

## ✅ Deployment Checklist

- [ ] Run migration: `python manage.py migrate`
- [ ] Backend starts without errors
- [ ] Can upload documents with `document_type` parameter
- [ ] Response includes all 10 new fields
- [ ] Frontend shows type detection & completeness
- [ ] Type mismatches trigger agent review
- [ ] Low completeness triggers agent review
- [ ] Test in production-like environment
- [ ] Monitor for AI accuracy
- [ ] Monitor agent review queue

---

## 🔗 Related Documents

- **DOCUMENT_TYPE_DETECTION_COMPLETE.md** - Full feature overview
- **DOCUMENT_TYPE_DETECTION_TESTING.md** - Testing guide with examples
- **IMPLEMENTATION_CHANGESET.md** - Detailed changeset by file

---

**Status:** ✅ Ready to Deploy

**Created:** January 2025
**Modified:** [Date]
**Version:** 1.0
