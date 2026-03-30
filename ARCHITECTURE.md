# Fizbo Seller Platform - Architecture Guide

## 📋 Overview

This is a professional, modular implementation of the Fizbo seller preparation platform built with Django (backend) and Next.js (frontend). Each module is isolated and can be developed/deployed independently.

---

## 🏗️ Backend Architecture (Django)

### Project Structure

```
backend_seller_platform/
├── shared/                          # Shared utilities (do not duplicate)
│   ├── constants/
│   │   └── theme.py                # Centralized theme, colors, tiers, documents
│   ├── exceptions/
│   │   └── __init__.py             # Custom exception classes
│   ├── utils/
│   │   └── helpers.py              # DateUtils, IDGenerator, ResponseUtils, etc.
│   └── middleware/                 # Custom middleware
│
├── modules/                         # Feature modules (isolated, scalable)
│   ├── doccheck/                   # Free assessment tool
│   │   ├── models.py               # DocCheckSession, DocCheckResult
│   │   ├── services.py             # Business logic (150 lines)
│   │   ├── serializers.py          # DRF serializers
│   │   ├── views.py                # API endpoints (< 100 lines)
│   │   └── urls.py
│   │
│   ├── docready/                   # Order & payment management
│   │   ├── models.py               # FizboOrder
│   │   ├── services.py             # Order lifecycle
│   │   ├── serializers.py          # Order serializers
│   │   ├── views.py                # Order endpoints
│   │   └── urls.py
│   │
│   ├── documents/                  # Document storage & lifecycle
│   │   ├── models.py               # Document model with expiry tracking
│   │   ├── services.py             # Upload, OCR, verification
│   │   ├── serializers.py          # Document serializers
│   │   ├── views.py                # Document endpoints
│   │   └── urls.py
│   │
│   ├── smartcma/                   # Price intelligence reports
│   │   ├── models.py               # CMAReport
│   │   ├── services.py             # Report generation
│   │   ├── serializers.py          # Report serializers
│   │   ├── views.py                # Report endpoints
│   │   └── urls.py
│   │
│   ├── operator/                   # Queue management & operations
│   │   ├── models.py               # OperatorQueue, OperatorNote
│   │   ├── services.py             # Queue & workflow management
│   │   ├── serializers.py          # Queue serializers
│   │   ├── views.py                # Operator endpoints
│   │   └── urls.py
│   │
│   └── payments/                   # Stripe integration
│       ├── models.py               # Payment entity
│       ├── services.py             # Stripe checkout, webhooks
│       ├── serializers.py          # Payment serializers
│       ├── views.py                # Payment endpoints
│       └── urls.py
│
└── myproject/                      # Django project settings
    ├── settings.py                # Configuration
    ├── urls.py                    # URL routing
    └── manage.py
```

### Key Principles

#### 1. **No Code Duplication**
- All shared logic lives in `shared/`
- Services are thin business logic wrappers
- Utilities are reusable across modules

#### 2. **Module Isolation**
Each module is self-contained:
- Models, Views, Services, Serializers, URLs
- Can be tested independently
- Can be deployed as separate microservice later

#### 3. **Smart Exceptions**
Custom exceptions with status codes:
```python
PaymentError("Payment failed", "PAYMENT_ERROR", 402)
DocumentError("OCR failed", "OCR_ERROR")
NotFoundError("Order", "FIZ-123-ABC")
```

#### 4. **Utility Functions**
Centralized helpers prevent duplication:
```python
from shared.utils import DateUtils, IDGenerator, ResponseUtils
from shared.constants import SERVICE_TIERS, DOCUMENT_TYPES
```

#### 5. **Line Limit**
Each file stays under 200 lines for readability.

---

## 🎨 Frontend Architecture (Next.js)

### Project Structure

```
frontend_seller_platform/src/
├── shared/                         # Global utilities & theme (no duplication)
│   ├── theme/
│   │   └── colors.ts              # Brand colors, tiers, documents, personas
│   ├── utils/
│   │   ├── api.ts                 # Centralized API client (all endpoints)
│   │   └── helpers.ts             # Format, validate, parse utilities
│   ├── types/
│   │   └── index.ts               # TypeScript interfaces
│   └── hooks/                      # Custom React hooks
│
├── components/                     # Reusable UI components
│   ├── Button.tsx                 # Button with variants
│   ├── Input.tsx                  # Input with validation
│   ├── Card.tsx                   # Card component
│   └── index.ts                   # Export all
│
├── modules/                        # Feature modules
│   ├── doccheck/
│   │   ├── components/
│   │   │   ├── DocCheckForm.tsx   # Assessment form
│   │   │   └── DocCheckResult.tsx # Results display
│   │   ├── page.tsx               # Module page
│   │   ├── store.ts               # Zustand state management
│   │   └── types.ts               # Module-specific types
│   │
│   ├── docready/
│   │   ├── components/
│   │   │   ├── OrderCard.tsx
│   │   │   └── TierSelector.tsx
│   │   ├── page.tsx
│   │   └── store.ts
│   │
│   ├── documents/
│   │   ├── components/
│   │   │   ├── DocumentUpload.tsx
│   │   │   └── DocumentList.tsx
│   │   ├── page.tsx
│   │   └── store.ts
│   │
│   ├── smartcma/
│   │   ├── components/
│   │   │   ├── ReportGenerator.tsx
│   │   │   └── ReportViewer.tsx
│   │   ├── page.tsx
│   │   └── store.ts
│   │
│   ├── payments/
│   │   ├── components/
│   │   │   ├── CheckoutForm.tsx
│   │   │   └── PaymentStatus.tsx
│   │   ├── page.tsx
│   │   └── store.ts
│   │
│   └── auth/
│       ├── components/
│       │   └── LoginForm.tsx
│       ├── page.tsx
│       └── store.ts
│
├── app/
│   ├── layout.tsx                 # Root layout
│   ├── page.tsx                   # Homepage
│   ├── globals.css                # Tailwind + theme CSS
│   └── [...routes]/page.tsx       # Module routing
│
├── store/                         # Global Zustand stores
│   ├── authStore.ts               # Authentication state
│   └── appStore.ts                # App-wide state
│
├── constants/
│   └── colors.ts                  # (Legacy - use shared/theme instead)
│
└── lib/
    └── api.ts                     # (Legacy - use shared/utils instead)
```

### Key Principles

#### 1. **Theme-First Design**
All colors, spacing, fonts defined in one file:
```typescript
import { BRAND_COLORS, SERVICE_TIERS, DOCUMENT_TYPES } from '@/shared/theme/colors';
```

#### 2. **Centralized API Client**
Single place for all API calls:
```typescript
import { apiClient } from '@/shared/utils/api';

await apiClient.createOrder(data);
await apiClient.uploadDocument(orderId, file);
await apiClient.createCheckout(paymentData);
```

#### 3. **Type Safety**
Shared TypeScript types across frontend:
```typescript
import type { Order, Document, ServiceTier } from '@/shared/types';
```

#### 4. **Module Isolation**
Each module has its own:
- Components
- State management (Zustand store)
- Pages/Routes
- Module-specific types

#### 5. **Component Patterns**
- Use server components (`'use client'` only when needed)
- Keep components under 150 lines
- Props typed with interfaces
- Reuse theme colors (no hardcoded hex)

---

## 📡 API Routes

### DocCheck Module
```
POST   /api/doccheck/start                    # Start assessment
GET    /api/doccheck/<session_id>/result      # Get results
```

### Orders (DocReady)
```
POST   /api/orders                            # Create order
GET    /api/orders/<order_id>                 # Get order
GET    /api/orders/seller/list                # List seller's orders
PATCH  /api/orders/<order_id>                 # Update order
```

### Documents
```
POST   /api/documents/<order_id>/upload       # Upload document
GET    /api/documents/<order_id>              # List documents
GET    /api/documents/<document_id>           # Get document details
```

### Payments
```
POST   /api/payments/checkout                 # Create Stripe session
GET    /api/payments/<session_id>/status      # Get payment status
POST   /api/payments/webhook                  # Stripe webhook
POST   /api/payments/refund                   # Request refund
```

### SmartCMA
```
POST   /api/cma/generate                      # Generate CMA report
GET    /api/cma/<report_id>                   # Get report
POST   /api/cma/<report_id>/export            # Export PDF
```

### Operator
```
GET    /api/operator/queue                    # Get operator queue
GET    /api/operator/<order_id>               # Get order details
PATCH  /api/operator/<order_id>/status        # Update status
POST   /api/operator/note                     # Add note
GET    /api/operator/blocked                  # Get blocked orders
```

---

## 🔐 Backend Response Format

All API responses follow consistent format:

**Success:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Order created",
  "data": { ... }
}
```

**Error:**
```json
{
  "status": "error",
  "code": 400,
  "error_code": "VALIDATION_ERROR",
  "message": "Email is required",
  "details": { "field": "email" }
}
```

---

## 🎯 Development Workflow

### Adding a Feature

1. **Define in shared/constants**
   ```python
   # shared/constants/theme.py
   NEW_FEATURE = { ... }
   ```

2. **Create module structure**
   ```
   modules/newfeature/
   ├── models.py
   ├── services.py
   ├── serializers.py
   ├── views.py
   └── urls.py
   ```

3. **Implement service layer** (business logic)
4. **Add serializers** (validation & transformation)
5. **Create views** (thin API layer, call services)
6. **Register in urls.py** and main Django urls

### Frontend Module

1. **Create shared types** if needed
2. **Create components** (under `modules/<feature>/components`)
3. **Create Zustand store** for state management
4. **Build page** that imports components
5. **Use apiClient** for all API calls

---

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```
DJANGO_SECRET_KEY=...
STRIPE_SECRET_KEY=...
DATABASE_URL=postgresql://...
SUPABASE_URL=...
SUPABASE_KEY=...
```

**Frontend (.env.local)**
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=...
```

---

## 📊 Database Models Relationships

```
┌─────────────────┐
│   DocCheckSession    │
│  (free assessment)   │
└─────────────────┘
        │
        └──→ DocCheckResult

┌─────────────────┐
│   FizboOrder     │◄──────────┐
│  (main entity)   │           │
└─────────────────┘           │
        │                       │
        ├──→ Document (many)    │
        │                       │
        ├──→ Payment ───────────┘
        │
        ├──→ CMAReport
        │
        └──→ OperatorQueue

┌─────────────────┐
│  OperatorNote    │
│  (attached to    │
│   FizboOrder)    │
└─────────────────┘
```

---

## ✅ Best Practices

### Backend
- ✅ Use services for business logic
- ✅ Keep views thin (< 50 lines)
- ✅ Validate in serializers, not views
- ✅ Use custom exceptions with codes
- ✅ Log important actions
- ✅ Keep files < 200 lines

### Frontend
- ✅ Use shared theme colors (no hardcoded hex)
- ✅ Centralize API calls in `apiClient`
- ✅ Use TypeScript for types
- ✅ Keep components < 150 lines
- ✅ Use Zustand for state
- ✅ Document complex logic

### General
- ✅ No code duplication
- ✅ DRY principle everywhere
- ✅ Consistent error handling
- ✅ Consistent naming conventions
- ✅ Module isolation
- ✅ Type safety (Python & TypeScript)

---

## 🚀 Deployment

### Backend
- Django + Gunicorn on Railway or Heroku
- PostgreSQL database
- Supabase for file storage
- Redis for caching (future)

### Frontend
- Next.js on Vercel
- Environment variables configured per environment
- API calls to backend service

---

## 📝 Module Responsibilities

| Module | Purpose | Owners |
|--------|---------|--------|
| **DocCheck** | Free assessment questionnaire | Frontend Dev |
| **DocReady** | Order management & tiers | Backend Dev |
| **Documents** | File storage & lifecycle | Backend Dev + DevOps |
| **SmartCMA** | Price intelligence reports | Data Dev |
| **Operator** | Queue & operations dashboard | Backend Dev + Operator |
| **Payments** | Stripe integration & webhooks | Backend Dev (Security) |

---

## 🔗 Links & Resources

- **Diagrams**: `/modules/` folder (use case, class, sequence diagrams)
- **API Docs**: Generated from DRF (Spectacular/Swagger)
- **Frontend**: `Next.js 15` with App Router
- **Styling**: Tailwind CSS + theme tokens
- **State**: Zustand (simple, zero-boilerplate)

---

Generated: March 2026
Confidence: Production-Ready ✅
