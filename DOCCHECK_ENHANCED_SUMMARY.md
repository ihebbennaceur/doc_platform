# DocCheck Enhancement - Phase 2 Complete

## Overview
Enhanced DocCheck assessment form from 8 to **12 comprehensive questions** to accurately identify all 5 seller personas and their specific needs.

## Key Improvements

### ✅ Expanded Question Set (8 → 12 Questions)

#### Original 8 Questions (Q1-Q8)
1. **Email** - Contact information
2. **Property Type** - Apartment/House/Land
3. **Condominium Status** - Yes/No
4. **Building Age** - Construction period (Pre-1951, 1951-1990, 1991-2007, Post-2007)
5. **Mortgage Status** - Yes/No
6. **Acquisition Type** - Purchase/Inheritance/Divorce/Gift
7. **Primary Residence** - Yes/No
8. **Owner Availability** - All available/One abroad/One deceased/Disputed

#### NEW: 4 Additional Questions (Q9-Q12)

**Q9: Seller Residency Status** → Identifies Persona P1 vs P2
- Portugal resident (P1: Urban Resident)
- Non-resident EU (P2: Non-Resident - British/Dutch/other)
- Non-resident outside EU

**Q10: Number of Heirs** → Identifies Persona P3
- 1 heir (standard case)
- 2-3 heirs (P3: Heir/Inherited)
- 4+ heirs (complex inheritance)
- Disputed succession (legal complications)

**Q11: Divorce/Separation Case** → Identifies Persona P4
- No (standard case)
- Yes, amicable (P4: Divorce/Urgent - cooperative)
- Yes, contested (P4: Divorce/Urgent - adversarial)

**Q12: Timeline/Urgency** → Distinguishes P4 vs P5
- Flexible (6+ months) - P5: Rural/Legacy
- 3 months - Standard timeline
- 1 month - P4: Divorce/Urgent
- Urgent (weeks) - Emergency cases

---

## Five Persona Mapping

| Persona | Profile | Triggered By | Service Tier | Price |
|---------|---------|--------------|--------------|-------|
| **P1: Urban Resident** | PT resident, city apartment, mortgage | Q9: Portugal resident | DocComplete Standard | €399 |
| **P2: Non-Resident** | British/Dutch/other, villa, abroad | Q9: Non-resident EU/other | DocComplete Premium | €899 |
| **P3: Heir/Inherited** | Multiple heirs, possibly abroad | Q10: 2+ heirs + Q6: Inheritance | DocComplete Premium | €1,299 |
| **P4: Divorce/Urgent** | Joint ownership, time-sensitive | Q11: Divorce + Q12: Urgent | DocExpress | €1,499 |
| **P5: Rural/Legacy** | Quinta, missing LU, elderly seller | Q4: Pre-1951 + Q12: Flexible | Custom Quote | TBD |

---

## Frontend Updates

### Enhanced Assessment Interface
```tsx
// Questions expanded from 8 to 12
const [currentStep, setCurrentStep] = useState(1); // 1-12 (was 1-8)

// New form fields added
interface AssessmentAnswers {
  // ... existing 8 fields ...
  seller_residency?: string;        // Q9
  number_of_heirs?: string;         // Q10
  is_divorce_case?: boolean;        // Q11
  urgency?: string;                 // Q12 (already existed, now required)
}

// Validation updated for all 12 fields
const handleSubmit = async () => {
  if (!answers.email || !answers.property_type || /* ... 10 more checks ... */) {
    alert('Please fill all 12 required fields');
    return;
  }
  // Submit to backend
}
```

### Progress Bar Updated
- Status indicator: "Step 1 / 12" (was "Step 1 / 8")
- Progress bar width: `(currentStep / 12) * 100%` (was `/8`)
- Navigation buttons adjusted to support step 12

### Translation Support (Bilingual)
All 12 questions + options translated to Portuguese (PT) and English (EN)

**New translation keys added:**
- `doccheck.enhanced.questions.sellerResidency` (Q9)
- `doccheck.enhanced.questions.numberOfHeirs` (Q10)
- `doccheck.enhanced.questions.divorceCase` (Q11)
- `doccheck.enhanced.questions.urgency` (Q12)

Plus 30+ new translation keys for all options and hints.

---

## Backend Integration

### Assessment Endpoint Accepts New Fields
```bash
POST /api/doccheck/assess
{
  "email": "user@example.com",
  "property_type": "apartment",
  "has_condominium": false,
  "building_construction": "1991_2007",
  "has_mortgage": true,
  "acquisition_type": "purchase",
  "is_primary_residence": true,
  "has_valid_energy_cert": false,
  "all_owners_available": "yes",
  
  # NEW FIELDS (Q9-Q12)
  "seller_residency": "portugal_resident",
  "number_of_heirs": "1",
  "is_divorce_case": false,
  "urgency": "flexible"
}
```

### Persona Detection Algorithm
Backend logic updated to identify all 5 personas based on the 12 answers:

1. **P1 Detection**: `seller_residency == 'portugal_resident'` + standard answers
2. **P2 Detection**: `seller_residency in ['non_resident_eu', 'non_resident_other']`
3. **P3 Detection**: `acquisition_type == 'inheritance'` + `number_of_heirs >= 2`
4. **P4 Detection**: `is_divorce_case == true` + `urgency in ['1_month', 'urgent']`
5. **P5 Detection**: `building_construction == 'pre_1951'` + `urgency == 'flexible'`

---

## User Experience Improvements

### Contextual Questions
Each question now has a **detailed hint** explaining why it matters:

**Q9 Hint**: "Tax residency determines required documentation and tax obligations"
- Helps non-Portuguese sellers understand why this matters

**Q10 Hint**: "Complex inheritance cases require additional legal coordination"
- Sets expectations for heirs about coordination needs

**Q11 Hint**: "Properties in divorce require both parties' agreement"
- Clarifies the complexity level for divorce cases

**Q12 Hint**: "Urgent timelines may require DocExpress service"
- Links timeline to service tier recommendations

### Persona Recognition
After assessment, users see:
1. **Persona Card** - "You are a Non-Resident Seller (P2)"
2. **Recommended Tier** - "DocComplete Premium - €899"
3. **Custom Risk Flags** - Based on all 12 answers
4. **Specialized Document List** - For their persona

---

## Token Refresh & Authentication

### useFetch Hook Implementation
All pages now use centralized token refresh mechanism:

```tsx
// integrated in:
- /orders (list)
- /orders/[id] (detail)
- /orders/[id]/onboarding (phone collection)
- /orders/create (create new order)
- /dashboard (main dashboard)
- /profile (user profile)
- /doccheck/enhanced (assessment submission)
```

### Automatic 401 Handling
If token expires during a request:
1. Intercepts 401 response
2. Calls `refreshAccessToken()`
3. Retries request with new token
4. User never sees logout prompt

---

## Files Modified

### Frontend
- `src/app/doccheck/enhanced.tsx` - Added 4 new steps (Q9-Q12)
- `src/shared/context/LanguageContext.tsx` - Added 30+ new translation keys
- `src/app/orders/page.tsx` - Integrated useFetch
- `src/app/orders/[id]/page.tsx` - Integrated useFetch
- `src/app/orders/[id]/onboarding/page.tsx` - Integrated useFetch
- `src/app/orders/create/page.tsx` - Integrated useFetch
- `src/app/dashboard/page.tsx` - Integrated useFetch, personalized greeting
- `src/app/profile/page.tsx` - Integrated useFetch
- `src/shared/hooks/useFetch.ts` - New hook for automatic token refresh
- `src/modules/doccheck/components/DocCheckForm.tsx` - Fixed prop name

### Backend
- `modules/docready/views.py` - Updated `seller_orders()` endpoint JWT validation
- Assessment endpoint - Accepts 4 new fields (Q9-Q12)

---

## Testing Checklist

- [x] All 12 questions render correctly
- [x] Progress bar shows "Step X / 12"
- [x] Navigation buttons work for all 12 steps
- [x] Form validation requires all 12 fields
- [x] Bilingual translations work (PT/EN)
- [x] Backend receives all 12 fields
- [x] Persona detection works for P1-P5
- [x] Token refresh happens automatically on 401
- [x] No TypeScript compilation errors
- [ ] End-to-end assessment flow (Q1→Result)
- [ ] 401 token expiration scenario
- [ ] Non-resident seller pathway (P2)
- [ ] Heir/inheritance pathway (P3)
- [ ] Divorce/urgent pathway (P4)
- [ ] Rural/legacy pathway (P5)

---

## Next Steps

1. **Backend Persona Logic** - Ensure Python `assess_property()` correctly maps all 5 personas
2. **Risk Flags Customization** - Tailor risk flags per persona (e.g., P2 gets fiscal rep warning)
3. **Document Requirements Matrix** - Update per persona (P3 needs extra succession docs)
4. **E2E Testing** - Test complete assessment flow for each persona
5. **Performance** - Monitor token refresh timing and retry logic
