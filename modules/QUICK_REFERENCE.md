# Fizbo Modules - Quick Reference Guide

## 📁 Directory Structure

```
modules/
├── README.md                          ← Start here (architecture overview)
│
├── 01_DocCheck/
│   ├── usecase_diagram.puml          (Assessment workflow)
│   ├── class_diagram.puml            (DocCheckSession, Results)
│   ├── sequence_diagram.puml         (Question flow)
│   └── README.md                     (Feature overview)
│
├── 02_DocReady/
│   ├── usecase_diagram.puml          (Order & tier selection)
│   ├── class_diagram.puml            (FizboOrder, Payment)
│   ├── sequence_diagram.puml         (Full checkout flow)
│   └── README.md                     (Payment & OCR integration)
│
├── 03_Documents/
│   ├── usecase_diagram.puml          (Upload, track, expire)
│   ├── class_diagram.puml            (FizboDocument lifecycle)
│   ├── sequence_diagram.puml         (Upload to expiry monitoring)
│   └── README.md                     (Storage & validity rules)
│
├── 04_SmartCMA/
│   ├── usecase_diagram.puml          (Report generation)
│   ├── class_diagram.puml            (Report sections)
│   ├── sequence_diagram.puml         (Valuation → PDF)
│   └── README.md                     (Price intelligence)
│
├── 05_Operator/
│   ├── usecase_diagram.puml          (Queue management)
│   ├── class_diagram.puml            (Dashboard entities)
│   ├── sequence_diagram.puml         (Order processing)
│   └── README.md                     (Operations procedures)
│
└── 06_Payments/
    ├── usecase_diagram.puml          (Checkout & refunds)
    ├── class_diagram.puml            (Payment entities)
    ├── sequence_diagram.puml         (Payment flow)
    └── README.md                     (Stripe integration)
```

## 🎯 Module Summary

| # | Module | Purpose | Users | Files |
|---|--------|---------|-------|-------|
| 1 | **DocCheck** | Free assessment tool | Sellers | 4 files |
| 2 | **DocReady** | Order & payment processing | Sellers | 4 files |
| 3 | **Documents** | Secure storage & lifecycle | All | 4 files |
| 4 | **SmartCMA** | Price intelligence report | Sellers | 4 files |
| 5 | **Operator** | Queue & operations dashboard | Operators | 4 files |
| 6 | **Payments** | Stripe integration & refunds | Sellers | 4 files |

**Total: 6 modules × 4 files = 24 diagram & documentation files**

---

## 🔍 How to Navigate

### If You Want to Understand...

**The complete buyer journey:**
1. `01_DocCheck/README.md` — How sellers discover documents
2. `02_DocReady/sequence_diagram.puml` — How they purchase
3. `03_Documents/sequence_diagram.puml` — How documents are managed
4. `04_SmartCMA/sequence_diagram.puml` — How they get pricing

**System architecture:**
1. `README.md` (this file) — System overview
2. `*/class_diagram.puml` — Entity relationships in each module

**Operator workflows:**
1. `05_Operator/README.md` — Operations manual
2. `05_Operator/sequence_diagram.puml` — Daily tasks

**Payment flows:**
1. `06_Payments/README.md` — Pricing and refunds
2. `06_Payments/sequence_diagram.puml` — Checkout to confirmation

---

## 📊 Diagram Types

### Use Case Diagrams
Show **actors** and their **interactions** with the system
- **Who**: Users (Seller, Operator, System)
- **What**: Actions and features
- **Outcome**: Goals achieved

**Example**: `05_Operator/usecase_diagram.puml` shows operator actions (view queue, update status, flag blocked)

### Class Diagrams
Show **entities** and their **relationships**
- **Properties**: Data attributes
- **Methods**: Operations
- **Relationships**: How entities connect

**Example**: `02_DocReady/class_diagram.puml` shows FizboOrder connects to Property, Payment, and SellerProfile

### Sequence Diagrams
Show **workflows** and **interactions over time**
- **Actors**: Users and system components
- **Messages**: API calls, database queries
- **Time**: Top-to-bottom progression

**Example**: `06_Payments/sequence_diagram.puml` shows payment flow from checkout to account creation

---

## 🔄 Module Interactions

```
SELLER JOURNEY:
┌─────────────┐     ┌──────────────┐     ┌──────────┐     ┌──────────┐
│ Arrives on  │────→│   DocCheck   │────→│ Payments │────→│ DocReady │
│   Website   │     │  (Free tool) │     │ (Stripe) │     │(Onboard) │
└─────────────┘     └──────────────┘     └──────────┘     └──────────┘
                                                                  │
                                                                  ↓
                           ┌──────────────┐     ┌──────────────┐
                           │  Operator    │────→│  Documents   │
                           │   (Queue)    │     │  (Tracking)  │
                           └──────────────┘     └──────────────┘
                                │                      │
                                └──────────┬───────────┘
                                           ↓
                           ┌──────────────────────────┐
                           │  SmartCMA (Price Report) │
                           └──────────────────────────┘
```

---

## 🛠 Tech Stack Reference

| Module | Frontend | Backend | Database | External |
|--------|----------|---------|----------|----------|
| DocCheck | React | FastAPI | Supabase | — |
| DocReady | Next.js | tRPC | Supabase | Stripe, OCR |
| Documents | React | tRPC | Supabase | Supabase Storage |
| SmartCMA | React | tRPC | Supabase | PropCheck, Reserva |
| Operator | React | tRPC | Supabase | Realtime, Inngest |
| Payments | React | tRPC | Supabase | Stripe |

---

## 📋 Key Business Rules by Module

### DocCheck
- 8 questions, < 90 seconds
- Email required only to view full result
- Service tier recommended automatically
- €100 discount if energy cert valid

### DocReady
- Three tiers: €399 (Standard) / €899 (Premium) / €1,499 (Express)
- Payment → Account created automatically
- Caderneta upload → OCR extraction → manual fallback
- Inngest workflow triggered post-payment

### Documents
- 8 document types with specific validity periods
- Status: missing → requested → pending → complete → expiring
- Expiry alerts: 30-day warning, 7-day critical

### SmartCMA
- Price band: low/mid/high with confidence score
- 3–5 comparable transactions (anonymised)
- Generated on demand after order completion
- PDF < 60 seconds

### Operator
- Daily routine: queue review → follow-up → status update
- 308 municipalities, each with different process
- Supplier coordination: peritos, solicitadores, câmaras
- No seller goes 48h without update

### Payments
- 23% VAT on all prices (VAT-exclusive display)
- Refund policy: 100% (5 days) / 50% (work started) / 0% (doc obtained)
- Stripe webhook signature verification required
- Zero card storage on Fizbo servers

---

## 🚀 Getting Started

### For Developers
1. Open `01_DocCheck/class_diagram.puml` to understand core entities
2. Review `README.md` for system architecture overview
3. Study sequence diagrams in order: DocCheck → DocReady → Documents → SmartCMA
4. Implement modules following data model and workflows

### For Product Managers
1. Read main `README.md` for feature overview
2. Review each module's `README.md` for detailed features
3. Check sequence diagrams to understand user experience

### For Operators
1. Read `05_Operator/README.md` completely (your operations manual)
2. Refer to `03_Documents/README.md` for document validity rules
3. Check `06_Payments/README.md` for refund policy

### For QA/Testers
1. Review all use case diagrams to identify test scenarios
2. Study sequence diagrams for expected interactions
3. Reference class diagrams for data validation rules

---

## 📞 Support & Questions

**Need clarification on a specific module?**
→ Check the module's README.md first

**Want to understand a workflow?**
→ Review the sequence_diagram.puml for that module

**Looking for data model?**
→ Check the class_diagram.puml

**Understanding user interactions?**
→ Review the usecase_diagram.puml

---

**Version**: 1.0  
**Created**: March 2026  
**Status**: Confidential — FAIRBANK Group
