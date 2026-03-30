# Fizbo Seller Platform - Modules Architecture

## Overview
This directory contains the complete module architecture for Fizbo, Portugal's first seller preparation platform. Each module is independently documented with **use case diagrams**, **class diagrams**, and **sequence diagrams**, providing a comprehensive understanding of system design.

## Modules

### 1. **DocCheck** (`01_DocCheck/`)
**Purpose**: Free assessment tool that helps sellers identify missing documents
- **Key Features**: 8-question assessment, document matrix, service tier recommendation, risk flags
- **Users**: Sellers (unauthenticated initially)
- **Artifacts**: 
  - `usecase_diagram.puml` - Assessment workflow use cases
  - `class_diagram.puml` - DocCheckSession, DocCheckResult, DocumentRequirement entities
  - `sequence_diagram.puml` - Question flow → result generation → email capture
  - `README.md` - Technical overview and data model

---

### 2. **DocReady** (`02_DocReady/`)
**Purpose**: End-to-end order management from tier selection through account creation and property onboarding
- **Key Features**: Stripe payment, OCR processing, automatic account creation, Inngest workflow trigger
- **Users**: Sellers (post-DocCheck)
- **Artifacts**:
  - `usecase_diagram.puml` - Tier selection, payment, onboarding, order tracking
  - `class_diagram.puml` - FizboOrder, SellerProfile, Property, PaymentSession entities
  - `sequence_diagram.puml` - Full checkout → OCR → workflow initiation flow
  - `README.md` - Payment handling, OCR integration, refund policy

---

### 3. **Documents** (`03_Documents/`)
**Purpose**: Complete document lifecycle management with secure storage and expiry monitoring
- **Key Features**: Status tracking, secure cloud storage, signed URLs, expiry alerts
- **Users**: Sellers, Operators
- **Artifacts**:
  - `usecase_diagram.puml` - Upload, verify, store, track, expire, download workflows
  - `class_diagram.puml` - FizboDocument, DocumentValidity, DocumentExpiryMonitor, StorageManager
  - `sequence_diagram.puml` - Upload → verification → status update → expiry monitoring
  - `README.md` - Storage architecture, validity rules, expiry monitoring

---

### 4. **SmartCMA** (`04_SmartCMA/`)
**Purpose**: Data-backed price intelligence report combining valuations, comparables, and market insights
- **Key Features**: Price band calculation, comparable transactions, market gap analysis, buyer heat signal, PDF export
- **Users**: Sellers (post-completion)
- **Artifacts**:
  - `usecase_diagram.puml` - Report generation, data aggregation, PDF export, off-market activation
  - `class_diagram.puml` - SmartCMAReport, PriceBand, Comparable, DaysOnMarket, BuyerHeat
  - `sequence_diagram.puml` - ValuationEngine → comparables → buyer pool → PDF generation
  - `README.md` - Report sections, integration with PropCheck and Reserva

---

### 5. **Operator** (`05_Operator/`)
**Purpose**: Real-time queue management dashboard for document procurement operations
- **Key Features**: Order queue, supplier coordination, status management, communication log
- **Users**: Fizbo operators (admin access)
- **Artifacts**:
  - `usecase_diagram.puml` - Queue management, document updates, supplier coordination, blocking
  - `class_diagram.puml` - OperatorQueue, OrderManagement, SupplierCoordination, CommunicationLog
  - `sequence_diagram.puml` - Queue review → document update → supplier booking → completion
  - `README.md` - Daily routine, supplier network, performance metrics

---

### 6. **Payments** (`06_Payments/`)
**Purpose**: Financial transaction handling with Stripe integration and refund management
- **Key Features**: Checkout session creation, dynamic pricing, VAT handling, webhook processing, refund policy
- **Users**: Sellers (payment phase)
- **Artifacts**:
  - `usecase_diagram.puml` - Price calculation, payment, webhook handling, refunds
  - `class_diagram.puml` - PaymentSession, PricingCalculator, RefundPolicy, StripeWebhookHandler
  - `sequence_diagram.puml` - Session creation → checkout → payment confirmation → account activation
  - `README.md` - Pricing tiers, refund policy, webhook events

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     FIZBO SELLER PLATFORM                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  DocCheck    │  │  Payments    │  │ SmartCMA     │          │
│  │  (Free tool) │  │  (Stripe)    │  │  (Price)     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                 │
│                     │                                           │
│              ┌──────▼────────┐                                 │
│              │   DocReady     │                                 │
│              │  (Order Flow)  │                                 │
│              └──────┬────────┘                                 │
│                     │                                           │
│         ┌───────────┼───────────┐                             │
│         │           │           │                             │
│  ┌──────▼─────┐ ┌──▼──────┐ ┌─▼──────────┐                  │
│  │ Documents  │ │Operator │ │  Workflows │                  │
│  │  (Storage) │ │Dashboard│ │  (Inngest) │                  │
│  └────────────┘ └─────────┘ └────────────┘                  │
│                                                                │
└─────────────────────────────────────────────────────────────────┘

Shared Infrastructure:
├── Supabase (Database + Storage)
├── Stripe (Payments)
├── Inngest (Workflows)
├── Resend + 360dialog (Notifications)
└── PropCheck + Reserva (External APIs)
```

## Data Flow

```
1. ACQUISITION
   Seller → DocCheck (free) → Email capture → Lead created

2. CONVERSION
   Lead → Tier selection → Payments module → Stripe checkout → Account created

3. ONBOARDING
   Account → DocReady (property upload) → OCR processing → Documents initialized

4. OPERATIONS
   Documents → Operator queue → Status updates → Notifications → Seller dashboard

5. COMPLETION & MONETIZATION
   Order complete → SmartCMA generation → Price report → Reserva activation

6. FINANCIAL
   Payment → Refund policy evaluation → Refund processing → Notification
```

## Key Entities Across Modules

| Entity | Owner Module | Used By | Purpose |
|--------|-------------|---------|---------|
| `FizboOrder` | DocReady | All | Core order aggregate |
| `FizboDocument` | Documents | Operator, DocReady | Document tracking |
| `SmartCMAReport` | SmartCMA | Seller, Operator | Price intelligence |
| `PaymentSession` | Payments | DocReady, Operator | Payment tracking |
| `OperatorQueue` | Operator | Operator, Backend | Task queue |
| `SellerProfile` | DocReady | Operator, Notifications | Seller preferences |
| `Property` | DocReady | All | Property metadata |

## Integration Points

### Module Dependencies
```
DocCheck → (leads to) → Payments
                           ↓
                        DocReady
                           ↓
                      ┌─────┴──────┐
                      ↓            ↓
                  Documents    Operator
                      ↓            ↓
                      └─────┬──────┘
                           ↓
                       SmartCMA
                           ↓
                      (Reserva CTA)
```

### External Integrations
- **Stripe**: Payment processing (Payments module)
- **Supabase**: Database and private storage (all modules)
- **Inngest**: Workflow orchestration (DocReady → Documents)
- **PropCheck**: Valuation engine (SmartCMA module)
- **Reserva**: Buyer pool and off-market listings (SmartCMA module)
- **Resend + 360dialog**: Email and WhatsApp notifications (all modules)

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 15 (App Router) | All user-facing pages |
| **API** | tRPC v11 | Type-safe backend routes |
| **Payment API** | FastAPI (Python) | DocCheck engine + OCR |
| **Database** | Supabase (PostgreSQL) | Schema: property_intelligence, personal_data, platform_ops |
| **Storage** | Supabase Storage | Private document storage |
| **Real-Time** | Supabase Realtime | Operator dashboard updates |
| **Workflows** | Inngest | Document procurement orchestration |
| **Payments** | Stripe | Card processing |
| **Notifications** | Resend + 360dialog | Email and WhatsApp |
| **PDF** | @react-pdf/renderer | SmartCMA report export |
| **Deployment** | Vercel | Next.js hosting |
| **Monitoring** | Sentry | Error tracking |

## How to Use These Diagrams

### For New Team Members
1. Start with this README for system overview
2. Read `01_DocCheck/README.md` for acquisition flow
3. Follow `02_DocReady/README.md` for order creation
4. Study `03_Documents` for data management
5. Review `05_Operator` for operations procedures

### For Developers
1. Check module README for data models
2. Review class diagrams for entity relationships
3. Study sequence diagrams for workflow implementation
4. Reference integration points in this file

### For Product Managers
1. Read module READMEs for feature descriptions
2. Review use case diagrams for user interactions
3. Check sequence diagrams for feature complexity

### For Operators
1. Focus on `05_Operator` module (queue management)
2. Reference `03_Documents` for document rules
3. Check notifications in `06_Payments` for payment confirmations

## Deployment & Scaling

### Phase 1 MVP (Weeks 1–12)
- All 6 modules deployed
- 40 orders/month target
- Single operator
- Basic supplier relationships

### Phase 2 (Month 6+)
- Automation improvements (more document automation)
- Supplier scaling (more perito partnerships)
- Team expansion (2+ operators)
- Geographic expansion (new municipalities)

## Contact & Support

For questions about module architecture:
- **DocCheck & DocReady**: Contact senior developer
- **Documents & Storage**: Contact backend lead
- **SmartCMA & Integrations**: Contact product lead
- **Operator Dashboard**: Contact operations lead
- **Payments & Stripe**: Contact payment specialist

---

**Document Version**: 1.0  
**Last Updated**: March 2026  
**Status**: Confidential — FAIRBANK Group
