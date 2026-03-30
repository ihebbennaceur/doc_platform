# 📋 Example Extraction Results

## Example 1: Successful Extraction - Caderneta Predial

### Request
```bash
curl -X POST http://127.0.0.1:8001/api/cases/dc_case_a1b2c3d4/documents/upload/ \
  -F "document_key=caderneta_predial" \
  -F "file=@caderneta_silva.pdf"
```

### Response (201 Created)
```json
{
  "document_key": "caderneta_predial",
  "status": "verified",
  "extraction_status": "success",
  "file_name": "caderneta_silva.pdf",
  "file_size": 2097152,
  "extracted_fields": {
    "name": "João Silva",
    "date_issued": "2022-05-10",
    "date_expiry": "2032-05-10",
    "issuer": "Câmara Municipal de Lisboa - Finanças",
    "reference_number": "0000123456",
    "property_reference": "PT001234/001"
  },
  "clarity_flag": "CLEAR",
  "clarity_assessment": {
    "is_clear": true,
    "legibility": 98,
    "overall_confidence": 96,
    "issues": []
  },
  "validity_flag": "VALID",
  "validity_assessment": {
    "is_valid": true,
    "is_expired": false,
    "validity_period_months": 120,
    "concerns": []
  },
  "confidence_score": 96,
  "extraction_notes": "Document is clear and legible. All required fields are present and machine-readable. Property registry number confirmed.",
  "operator_notes": "",
  "needs_manual_review": false,
  "all_fields_present": true,
  "expiry_date": "2032-05-10",
  "is_expired": false,
  "uploaded_at": "2026-03-30T10:30:00Z",
  "extracted_at": "2026-03-30T10:31:15Z",
  "extraction_error": null
}
```

### Frontend Display
```
📄 Caderneta Predial        ✓ VERIFIED
┌─────────────────────────────────────┐
│ 🏠 Caderneta Predial                 │
│    caderneta_silva.pdf               │
│                                       │
│ ✓ VERIFIED (Status badge - green)   │
│                                       │
│ Extracted Data:                       │
│ 📥 Name: João Silva                 │
│ 💼 Issuer: Câmara Municipal Lisboa  │
│ 📅 Issued: 2022-05-10               │
│ 📅 Expires: 2032-05-10              │
│                                       │
│ [🟢 CLEAR 96%] [🟢 VALID]          │
│                                       │
│ ✅ All fields present                │
│ ✅ No manual review needed           │
└─────────────────────────────────────┘
```

---

## Example 2: Extraction Needs Review - Partial Clarity

### Response (201 Created)
```json
{
  "document_key": "certidao_permanente",
  "status": "extracted",
  "extraction_status": "success",
  "file_name": "certidao_old_scan.pdf",
  "file_size": 1048576,
  "extracted_fields": {
    "name": "Maria Santos",
    "date_issued": "2010-03-15",
    "date_expiry": null,
    "issuer": "Cartório de Registos Prediais - [UNCLEAR]",
    "reference_number": "PT0087654/001",
    "property_reference": null
  },
  "clarity_flag": "PARTIAL",
  "clarity_assessment": {
    "is_clear": false,
    "legibility": 62,
    "overall_confidence": 65,
    "issues": [
      "Document is scanned/low resolution",
      "Issuer name partially obscured",
      "Property reference section not visible",
      "Stamp partially faded"
    ]
  },
  "validity_flag": "NOT_ASSESSED",
  "validity_assessment": {
    "is_valid": null,
    "is_expired": false,
    "validity_period_months": null,
    "concerns": [
      "Cannot determine validity due to unclear issuer",
      "No expiry date found - may be permanent",
      "Property reference missing - cannot cross-reference"
    ]
  },
  "confidence_score": 65,
  "extraction_notes": "Document quality is poor (scanned/low-res). Extracted name with confidence, but issuer name is partially unclear. Property reference not visible. Recommend operator review with original document.",
  "operator_notes": "",
  "needs_manual_review": true,
  "all_fields_present": false,
  "expiry_date": null,
  "is_expired": false,
  "uploaded_at": "2026-03-30T11:00:00Z",
  "extracted_at": "2026-03-30T11:00:45Z",
  "extraction_error": null
}
```

### Frontend Display
```
📄 Certidão Permanente      ⚠️ EXTRACTED
┌─────────────────────────────────────┐
│ 📋 Certidão Permanente              │
│    certidao_old_scan.pdf             │
│                                       │
│ ⚠️ EXTRACTED - Awaiting Review      │
│                                       │
│ Extracted Data:                       │
│ 📥 Name: Maria Santos               │
│ 💼 Issuer: [UNCLEAR]                │
│ 📅 Issued: 2010-03-15               │
│                                       │
│ [🟡 PARTIAL 65%] [❓ NOT_ASSESSED]  │
│                                       │
│ ⚠️ Requires manual operator review   │
│                                       │
│ Issues detected:                      │
│ • Document is scanned/low resolution │
│ • Issuer name partially obscured     │
│ • Property reference not visible     │
│                                       │
│ Operator Notes:                       │
│ [Text area for manual notes]         │
└─────────────────────────────────────┘
```

---

## Example 3: Extraction Failed - Error Handling

### Response (201 Created - with error)
```json
{
  "document_key": "certificado_energetico",
  "status": "uploaded",
  "extraction_status": "failed",
  "file_name": "corrupt_file.pdf",
  "file_size": 256,
  "extracted_fields": {},
  "clarity_flag": "NOT_ASSESSED",
  "clarity_assessment": {},
  "validity_flag": "NOT_ASSESSED",
  "validity_assessment": {},
  "confidence_score": 0,
  "extraction_notes": "",
  "operator_notes": "",
  "needs_manual_review": true,
  "all_fields_present": false,
  "expiry_date": null,
  "is_expired": false,
  "uploaded_at": "2026-03-30T12:00:00Z",
  "extracted_at": null,
  "extraction_error": "Failed to process file: PDF appears to be corrupted or encrypted. Manual review required."
}
```

### Frontend Display
```
📄 Certificado Energético   ⚠️ UPLOADED
┌─────────────────────────────────────┐
│ ⚡ Certificado Energético           │
│    corrupt_file.pdf                  │
│                                       │
│ ⚠️ UPLOADED                          │
│                                       │
│ ❌ Extraction failed                 │
│ "PDF appears corrupted or encrypted" │
│ "Manual review required"              │
│                                       │
│ Operator Notes:                       │
│ [Text area for manual notes]         │
│                                       │
│ Next step: Operator must manually     │
│ review the file or ask seller to     │
│ resubmit a clear copy                │
└─────────────────────────────────────┘
```

---

## Example 4: Document Expired

### Response (201 Created)
```json
{
  "document_key": "certificado_energetico",
  "status": "expired",
  "extraction_status": "success",
  "file_name": "energy_cert_2019.pdf",
  "file_size": 987654,
  "extracted_fields": {
    "name": "João Silva",
    "date_issued": "2019-08-20",
    "date_expiry": "2024-08-20",
    "issuer": "ADENE - Agência da Energia",
    "reference_number": "PT2019-87654",
    "property_reference": "PT001234/001"
  },
  "clarity_flag": "CLEAR",
  "clarity_assessment": {
    "is_clear": true,
    "legibility": 94,
    "overall_confidence": 94,
    "issues": []
  },
  "validity_flag": "EXPIRED",
  "validity_assessment": {
    "is_valid": false,
    "is_expired": true,
    "validity_period_months": 60,
    "concerns": [
      "Document expired on 2024-08-20",
      "Certificate is now 584 days overdue",
      "A new energy certificate must be obtained before sale"
    ]
  },
  "confidence_score": 94,
  "extraction_notes": "Certificate clearly readable, but validity has expired. This document cannot be used for property sale.",
  "operator_notes": "",
  "needs_manual_review": false,
  "all_fields_present": true,
  "expiry_date": "2024-08-20",
  "is_expired": true,
  "uploaded_at": "2026-03-30T13:00:00Z",
  "extracted_at": "2026-03-30T13:00:30Z",
  "extraction_error": null
}
```

### Frontend Display
```
📄 Certificado Energético   ❌ EXPIRED
┌─────────────────────────────────────┐
│ ⚡ Certificado Energético           │
│    energy_cert_2019.pdf              │
│                                       │
│ ❌ EXPIRED (Status badge - red)     │
│                                       │
│ Extracted Data:                       │
│ 📥 Name: João Silva                 │
│ 💼 Issuer: ADENE                    │
│ 📅 Issued: 2019-08-20               │
│ 📅 Expired: 2024-08-20              │
│                                       │
│ [🟢 CLEAR 94%] [🔴 EXPIRED]        │
│                                       │
│ ⚠️ Expired 584 days ago              │
│ ℹ️ New certificate must be obtained  │
│                                       │
│ Action needed: Ask seller to obtain  │
│ a new energy certificate             │
└─────────────────────────────────────┘
```

---

## Example 5: Multiple Issues - Complex Case

### Response (201 Created)
```json
{
  "document_key": "declaracao_condominio",
  "status": "extracted",
  "extraction_status": "success",
  "file_name": "condominio_declaration_photo.jpg",
  "file_size": 3145728,
  "extracted_fields": {
    "name": "Condomínio do Parque Residence",
    "date_issued": "2025-10-15",
    "date_expiry": "2026-10-15",
    "issuer": "[MULTIPLE SIGNATURES - UNCLEAR]",
    "reference_number": "CONDO-2025-PT-987654",
    "property_reference": "Unit 5B - 3rd Floor"
  },
  "clarity_flag": "UNCLEAR",
  "clarity_assessment": {
    "is_clear": false,
    "legibility": 38,
    "overall_confidence": 42,
    "issues": [
      "Photo taken at an angle (perspective distortion)",
      "Lighting is poor (shadows across document)",
      "Document is crumpled and worn",
      "Multiple signatures partially obscured",
      "Bottom section cut off in photo",
      "Handwritten annotations overlap text"
    ]
  },
  "validity_flag": "INVALID",
  "validity_assessment": {
    "is_valid": false,
    "is_expired": false,
    "validity_period_months": 12,
    "concerns": [
      "Multiple required signatures are missing or illegible",
      "Document appears to be a photocopy of a photocopy",
      "Condominium representative seal not visible",
      "Required notarization seal cannot be verified",
      "Bottom section missing - may contain important information"
    ]
  },
  "confidence_score": 42,
  "extraction_notes": "Poor quality image submission. Document appears to be a casual phone photo taken at an angle with inadequate lighting. Multiple critical elements are unclear or missing. This document cannot be validated in its current form. Recommend obtaining an official certified copy from the condominium administration.",
  "operator_notes": "",
  "needs_manual_review": true,
  "all_fields_present": false,
  "expiry_date": "2026-10-15",
  "is_expired": false,
  "uploaded_at": "2026-03-30T14:00:00Z",
  "extracted_at": "2026-03-30T14:00:50Z",
  "extraction_error": null
}
```

### Frontend Display
```
📄 Declaração Condomínio    ❌ INVALID
┌─────────────────────────────────────┐
│ 📋 Declaração Condomínio             │
│    condominio_declaration_photo.jpg  │
│                                       │
│ ❌ INVALID - Awaiting Resubmission  │
│                                       │
│ Extracted Data:                       │
│ 📥 Name: Condomínio Parque Residenc │
│ 💼 Issuer: [MULTIPLE SIGS - ?]      │
│ 📅 Issued: 2025-10-15               │
│                                       │
│ [🔴 UNCLEAR 42%] [🔴 INVALID]       │
│                                       │
│ ⚠️ Requires manual operator review   │
│                                       │
│ Issues detected (6 found):            │
│ • Photo taken at an angle             │
│ • Poor lighting (shadows)             │
│ • Document crumpled and worn          │
│ • Multiple signatures obscured         │
│ • Bottom section cut off              │
│ • Handwritten annotations overlap     │
│                                       │
│ AI Assessment:                        │
│ This is a casual phone photo, not an │
│ official document. Multiple critical │
│ elements are missing or unclear.      │
│                                       │
│ Recommended Action:                   │
│ Ask seller to submit an official      │
│ certified copy from the condominium   │
│ administration.                       │
│                                       │
│ Operator Notes:                       │
│ [Text area for notes]                │
└─────────────────────────────────────┘
```

---

## Clarity & Validity Scale

### Clarity Levels
```
🟢 CLEAR (90-100%)
   ✅ Document is sharp and legible
   ✅ All text readable
   ✅ No shadows or glare
   ✅ Good contrast
   ✅ Professional quality scan/photo

🟡 PARTIAL (60-89%)
   ⚠️ Some parts clear, some unclear
   ⚠️ Minor shadows or glare
   ⚠️ Some text partially faded
   ⚠️ Adequate for most purposes
   ⚠️ May need secondary review for critical fields

🔴 UNCLEAR (0-59%)
   ❌ Document is difficult to read
   ❌ Significant shadows/glare/distortion
   ❌ Poor lighting or focus
   ❌ Requires manual review
   ❌ May need high-quality resubmission
```

### Validity Levels
```
🟢 VALID
   ✅ Document is current
   ✅ Not expired
   ✅ All required fields present
   ✅ No concerns identified

❓ NOT_ASSESSED
   ⚠️ Cannot determine validity
   ⚠️ Clarity too poor to assess
   ⚠️ Requires manual verification
   ⚠️ Flagged for operator review

🟡 NEEDS_REVIEW (Mixed)
   ⚠️ Expiry date approaching (< 30 days)
   ⚠️ Some concerns but not expired
   ⚠️ Recommend verification

🔴 EXPIRED
   ❌ Document validity has passed
   ❌ Cannot be used for transactions
   ❌ Requires renewal

🔴 INVALID
   ❌ Document does not meet requirements
   ❌ Missing required elements
   ❌ Concerns that prevent usage
```

---

## Operator Action Required Scenarios

### Scenario 1: Clear & Valid → Auto Approve
```
Status: VERIFIED
Action: None needed - document accepted automatically
Next: Send confirmation to seller
```

### Scenario 2: Clear but Flagged → Manual Approval
```
Status: EXTRACTED
Clarity: CLEAR
Validity: NOT_ASSESSED
Action: Operator reviews and clicks VERIFY
Next: Send approval to seller
```

### Scenario 3: Unclear → Request Resubmission
```
Status: EXTRACTED
Clarity: UNCLEAR
Validity: NOT_ASSESSED
Action: Operator adds note "Please submit clearer photo"
Next: Send rejection with instructions to seller
```

### Scenario 4: Expired → Request Renewal
```
Status: EXPIRED
Clarity: CLEAR
Validity: EXPIRED
Action: Operator notes "Certificate expired - renew with ADENE"
Next: Send renewal instructions to seller
```

---

This demonstrates the complete extraction result types your system will handle!
