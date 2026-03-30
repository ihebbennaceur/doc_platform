# DocCheck Enhanced - Testing Guide

## Quick Start: Test the Enhanced DocCheck Form

### Pre-requisites
- Frontend running on `localhost:3000`
- Backend running on `localhost:8000`
- User logged in (or redirected to login)

---

## Test Scenarios

### Scenario 1: P1 - Urban Resident (Portugal)
**Expected Persona**: P1 Urban Resident → DocComplete Standard €399

```
Q1. Email: joao@example.com
Q2. Property Type: apartment
Q3. Condominium: yes
Q4. Building Age: 1991_2007
Q5. Mortgage: yes
Q6. Acquisition: purchase
Q7. Primary Residence: yes
Q8. Owners Available: yes
Q9. Seller Residency: portugal_resident ← KEY
Q10. Number of Heirs: 1
Q11. Divorce Case: no
Q12. Urgency: flexible
```

**Expected Result:**
- Persona: "Urban Resident (P1)"
- Tier: "DocComplete Standard - €399"
- Risk flags: Mortgage discharge required
- Doc list: deed, mortgage certificate, energy cert, etc.

---

### Scenario 2: P2 - Non-Resident (British/Dutch)
**Expected Persona**: P2 Non-Resident → DocComplete Premium €899

```
Q1. Email: david@example.co.uk
Q2. Property Type: house
Q3. Condominium: no
Q4. Building Age: post_2007
Q5. Mortgage: no
Q6. Acquisition: purchase
Q7. Primary Residence: no
Q8. Owners Available: one_abroad ← KEY
Q9. Seller Residency: non_resident_eu ← KEY
Q10. Number of Heirs: 1
Q11. Divorce Case: no
Q12. Urgency: flexible
```

**Expected Result:**
- Persona: "Non-Resident Seller (P2)"
- Tier: "DocComplete Premium - €899"
- Risk flags: 
  - Fiscal representation required (non-resident tax)
  - Power of attorney may be needed
  - Remote handling arranged
- Doc list: deed, fiscal rep appointment, POA if needed

---

### Scenario 3: P3 - Heir/Inherited Property
**Expected Persona**: P3 Heir/Inherited → DocComplete Premium €1,299

```
Q1. Email: maria@example.com
Q2. Property Type: house
Q3. Condominium: no
Q4. Building Age: pre_1951
Q5. Mortgage: no
Q6. Acquisition: inheritance ← KEY
Q7. Primary Residence: no
Q8. Owners Available: disputed ← KEY
Q9. Seller Residency: portugal_resident
Q10. Number of Heirs: 4_or_more ← KEY
Q11. Divorce Case: no
Q12. Urgency: flexible
```

**Expected Result:**
- Persona: "Heir/Inherited Property (P3)"
- Tier: "DocComplete Premium - €1,299"
- Risk flags:
  - Multiple heirs coordination required
  - Succession certificate may be needed
  - Notarization of all heir consents
  - Potential international heirs (extra complexity)
- Doc list: succession certificate, all heirs' IDs, notarized consents

---

### Scenario 4: P4 - Divorce/Urgent Case
**Expected Persona**: P4 Divorce/Urgent → DocExpress €1,499

```
Q1. Email: carlos@example.com
Q2. Property Type: apartment
Q3. Condominium: yes
Q4. Building Age: 1951_1990
Q5. Mortgage: yes
Q6. Acquisition: divorce ← KEY
Q7. Primary Residence: yes
Q8. Owners Available: disputed ← KEY
Q9. Seller Residency: portugal_resident
Q10. Number of Heirs: 1
Q11. Divorce Case: yes_contested ← KEY
Q12. Urgency: 1_month ← KEY (URGENT)
```

**Expected Result:**
- Persona: "Divorce/Urgent Seller (P4)"
- Tier: "DocExpress - €1,499"
- Risk flags:
  - Both spouses must sign sale agreement
  - Court approval may be needed (contested)
  - 30-day expedited processing
  - Escrow account may be required
- Doc list: divorce decree, both parties' IDs, deed, mortgage cert, ex-spouse signature on sale

---

### Scenario 5: P5 - Rural/Legacy Property
**Expected Persona**: P5 Rural/Legacy → Custom Quote

```
Q1. Email: silva@example.com
Q2. Property Type: land
Q3. Condominium: no
Q4. Building Age: pre_1951 ← KEY
Q5. Mortgage: no
Q6. Acquisition: inheritance
Q7. Primary Residence: no
Q8. Owners Available: one_deceased ← KEY
Q9. Seller Residency: portugal_resident
Q10. Number of Heirs: 2_3
Q11. Divorce Case: no
Q12. Urgency: flexible ← KEY
```

**Expected Result:**
- Persona: "Rural/Legacy Property (P5)"
- Tier: "Custom Quote (contact sales)"
- Risk flags:
  - Missing land unit (LU) registration
  - Elderly seller may need assistance
  - Complex succession from deceased heir
  - May require surveyor assessment
  - Longer timeline recommended (3-6 months)
- Doc list: Deed with LU gaps noted, old succession docs, neighbor confirmations possibly needed

---

## Manual Testing Steps

### 1. **Test Bilingual Support**
1. Go to `/doccheck/enhanced`
2. Click language switcher (PT/EN)
3. Verify all 12 questions display in correct language
4. Verify all hints display in correct language

### 2. **Test Progress Bar**
1. Start assessment
2. After Q1, progress bar should show: `Step 1 / 12` and `~8%` filled
3. Go to Q6: Should show `Step 6 / 12` and `~50%` filled
4. Go to Q12: Should show `Step 12 / 12` and `~100%` filled

### 3. **Test Navigation**
1. Q1 → Click Next → Go to Q2 (Previous button should be enabled)
2. Q2 → Click Previous → Go back to Q1 (Previous button should be disabled)
3. Q12 → "Next" button should change to "View Result" (submit button)

### 4. **Test Validation**
1. Q1 (Email): Skip it, click Next → Should allow (non-required field in some forms)
2. Q2 (Property Type): Skip it, try to submit → Error message
3. Fill some fields, leave Q9/Q10/Q11/Q12 blank, try to submit → Error message

### 5. **Test Persona Detection**
Complete each of the 5 scenarios above and verify:
- Correct persona name displayed
- Correct tier recommended
- Correct risk flags shown
- Correct document list

### 6. **Test Backend Integration**
1. Open browser DevTools → Network tab
2. Complete assessment
3. Watch POST to `/api/doccheck/assess`
4. Verify all 12 fields in request body:
   - Q1-8: Original fields
   - Q9: `seller_residency`
   - Q10: `number_of_heirs`
   - Q11: `is_divorce_case`
   - Q12: `urgency`

### 7. **Test Token Refresh** (Advanced)
1. Start assessment
2. Open browser DevTools → Storage → localStorage
3. Find `access_token`, manually expire it (edit or delete)
4. Continue to next step - should auto-refresh
5. Verify no 401 error displayed to user

---

## Expected Outputs

### Successful Assessment Response (Backend)
```json
{
  "data": {
    "email": "user@example.com",
    "persona": {
      "slug": "urban_resident",
      "name": "Urban Resident",
      "description": "Portugal resident with city property",
      "recommended_tier": "standard"
    },
    "missing_documents": [
      "Mortgage certificate (Certificado do Registo de Penhora)",
      "Condominium minutes (Ata de condomínio)"
    ],
    "missing_document_count": 2,
    "recommended_tier": {
      "slug": "standard",
      "name": "DocComplete Standard",
      "price": 399
    },
    "risk_flags": [
      {
        "key": "mortgage_discharge",
        "message": "Property has active mortgage",
        "recommendation": "Bank discharge required before sale",
        "severity": "high"
      }
    ],
    "has_risk_flags": true,
    "summary": {
      "documents_always_required": 8,
      "documents_missing_count": 2,
      "risk_flag_count": 1,
      "is_free_tier": false,
      "is_urgent": false
    }
  }
}
```

### Error Response (Missing Fields)
```json
{
  "error": "Missing required fields",
  "missing": [
    "seller_residency",
    "urgency"
  ]
}
```

---

## Browser Console Checks

After submitting assessment, you should see:
```
[DocCheckEnhanced] Submitting assessment: {
  email: "user@example.com",
  property_type: "apartment",
  ...
  seller_residency: "portugal_resident",
  number_of_heirs: "1",
  is_divorce_case: false,
  urgency: "flexible"
}
[DocCheckEnhanced] Response status: 200
[DocCheckEnhanced] Success: {...result data...}
```

---

## Debugging Tips

### If questions not appearing:
1. Check browser console for errors
2. Verify translation keys exist in LanguageContext
3. Check `renderStep9/10/11/12` functions defined

### If progress bar wrong:
1. Verify `currentStep` state updating (DevTools React plugin)
2. Check progress calc: `(currentStep / 12) * 100%`

### If submission fails:
1. Check backend `/api/doccheck/assess` endpoint
2. Verify all 12 fields sent in request body
3. Check backend error logs

### If persona wrong:
1. Backend persona detection logic might be off
2. Check `assess_property()` function in Python
3. Verify each condition for P1-P5 detection

---

## Performance Notes

- Form renders instantly (no loading on each step)
- Submission takes ~1-2 seconds (includes backend processing)
- Progress bar animates smoothly
- Language switch is instant (uses React context)
- Navigation between steps is instant

---

## Known Limitations

- Form does not auto-save progress (if user navigates away, answers lost)
- No estimated time display per question
- Risk flags don't link to detailed help articles yet
- No real-time validation (only on submit)

---

## Next: Create Order

After successful assessment, user sees "Proceed with This Plan" button which should:
1. Navigate to `/orders/create?tier=standard` (or premium/express)
2. Pre-select the recommended tier
3. Ask for confirmation and payment
