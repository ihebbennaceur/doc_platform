# Quick Reference - Fizbo Platform Development

## 🚀 Quick Start

### Backend Setup
```bash
cd backend_django/backend_seller_platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend_seller_platform

# Install dependencies
npm install

# Run dev server
npm run dev

# Open http://localhost:3000
```

---

## 📁 File Structure Quick Guide

### Backend - What Goes Where?

```
models.py          → Entity definitions (only models & relationships)
                   Max 50 lines per model

services.py        → Business logic, calculations, workflows
                   Main file for feature logic
                   Use utilities from shared/

serializers.py     → Input validation, field transformations
                   Use DRF validators

views.py           → API endpoints (call services, return responses)
                   Keep views thin (20-30 lines each)
                   Use ResponseUtils for consistency

urls.py            → Route definitions

shared/            → Reusable code (exceptions, utils, constants)
                   DO NOT duplicate across modules
```

### Frontend - What Goes Where?

```
shared/theme/colors.ts    → All brand colors, sizes, tier definitions
                          Use here: BRAND_COLORS, SERVICE_TIERS

shared/utils/api.ts       → All API endpoints
                          Use here: POST, GET, PATCH

shared/utils/helpers.ts   → Utility functions (format, validate)
                          Use here: formatCurrency, validateEmail

shared/types/index.ts     → TypeScript interfaces
                          Use here: Order, Document, Payment

modules/[feature]/components/   → Feature components
modules/[feature]/page.tsx      → Feature page
modules/[feature]/store.ts      → Zustand state for feature
```

---

## 💡 Common Code Patterns

### Backend Service (300 lines max)
```python
# services.py
from shared.constants import SERVICE_TIERS
from shared.utils import IDGenerator, DateUtils, ResponseUtils
from shared.exceptions import ValidationError, NotFoundError

class OrderService:
    @staticmethod
    def create_order(email: str, tier: str) -> Order:
        # Validate
        if tier not in SERVICE_TIERS:
            raise ValidationError("Invalid tier")
        
        # Create
        order = Order.objects.create(
            id=IDGenerator.order_id(),
            email=email,
            tier=tier
        )
        
        # Log
        LoggingUtils.log_action("order_created", details={"order_id": order.id})
        
        return order
```

### Backend View (< 100 lines)
```python
# views.py
@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    try:
        order = OrderService.create_order(**serializer.validated_data)
        return Response(
            ResponseUtils.success(OrderSerializer(order).data),
            status=201
        )
    except ValidationError as e:
        return Response(
            ResponseUtils.error(e.message),
            status=e.status_code
        )
```

### Frontend Component (< 150 lines)
```typescript
// components/OrderForm.tsx
'use client';

import { useState } from 'react';
import { Button } from '@/components/Button';
import { Input } from '@/components/InputComponent';
import { Card } from '@/components/CardComponent';
import { apiClient } from '@/shared/utils/api';
import { BRAND_COLORS } from '@/shared/theme/colors';

export const OrderForm = () => {
  const [loading, setLoading] = useState(false);
  
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await apiClient.createOrder(/* data */);
      // Success
    } catch (error) {
      // Error handling
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <Card style={{ backgroundColor: BRAND_COLORS.background }}>
      <form onSubmit={handleSubmit}>
        {/* Form fields */}
        <Button type="submit" disabled={loading}>Create Order</Button>
      </form>
    </Card>
  );
};
```

---

## 🔑 Key Imports

### Backend
```python
# Constants
from shared.constants import (
    SERVICE_TIERS,
    DOCUMENT_TYPES,
    ORDER_STATUS,
    SELLER_PERSONAS
)

# Utilities
from shared.utils import (
    IDGenerator,      # UUID, order IDs, short IDs
    DateUtils,        # Add months, check expiry
    ResponseUtils,    # Success/error responses
    ValidationUtils,  # Email, phone, NIF validation
    FileUtils,        # File validation, storage paths
    LoggingUtils      # Log actions and errors
)

# Exceptions
from shared.exceptions import (
    ValidationError,
    NotFoundError,
    PaymentError,
    DocumentError,
    OCRError
)
```

### Frontend
```typescript
// Theme & Constants
import { BRAND_COLORS, SERVICE_TIERS, DOCUMENT_TYPES } from '@/shared/theme/colors';

// API
import { apiClient } from '@/shared/utils/api';

// Utilities
import { formatCurrency, validateEmail, formatDate } from '@/shared/utils/helpers';

// Types
import type { Order, Document, ServiceTier } from '@/shared/types';

// Components
import { Button } from '@/components/Button';
import { Card } from '@/components/CardComponent';
import { Input } from '@/components/InputComponent';
```

---

## 📋 Checklist - Adding a New Feature

### Backend
- [ ] Create `modules/feature/` folder
- [ ] Define models in `models.py`
- [ ] Implement business logic in `services.py`
- [ ] Create serializers in `serializers.py`
- [ ] Write views/endpoints in `views.py` (keep thin!)
- [ ] Define routes in `urls.py`
- [ ] Create `apps.py` and `__init__.py`
- [ ] Register in Django settings `INSTALLED_APPS`
- [ ] Write tests
- [ ] Document API endpoints

### Frontend
- [ ] Create `modules/feature/` folder
- [ ] Create `components/` subfolder
- [ ] Build components (< 150 lines each)
- [ ] Create `store.ts` for state management
- [ ] Create `page.tsx` for module page
- [ ] Add types to shared if reusable
- [ ] Use `apiClient` for all API calls
- [ ] Use `BRAND_COLORS` for styling
- [ ] Test all user flows

---

## 🎨 Theme Usage Examples

### Backend (Python)
```python
from shared.constants.theme import (
    BRAND_COLORS,
    SERVICE_TIERS,
    DOCUMENT_TYPES
)

# Get color
color = BRAND_COLORS["primary"]  # "#2E5D4B"

# Get tier
tier = SERVICE_TIERS.get("standard")
print(tier["price"])  # 399

# Get document
doc = DOCUMENT_TYPES.get("caderneta")
print(doc["validity_months"])  # 12
```

### Frontend (TypeScript)
```typescript
import { BRAND_COLORS, SERVICE_TIERS, formatCurrency } from '@/shared/theme/colors';

// In component
<div style={{ backgroundColor: BRAND_COLORS.primary }}>
  {SERVICE_TIERS.premium.name}
  {formatCurrency(SERVICE_TIERS.premium.price)}
</div>

// In Tailwind
<div className="bg-primary text-white px-lg py-md">
  {/* Uses Tailwind config extended with our theme */}
</div>
```

---

## 🔗 API Response Structure

### Success Response
```json
{
  "status": "success",
  "code": 200,
  "message": "Order created successfully",
  "data": {
    "id": "FIZ-20260317-ABC123",
    "email": "seller@example.com",
    "status": "draft"
  }
}
```

### Error Response
```json
{
  "status": "error",
  "code": 400,
  "error_code": "VALIDATION_ERROR",
  "message": "Invalid service tier",
  "details": {
    "field": "service_tier",
    "value": "invalid"
  }
}
```

### Paginated Response
```json
{
  "status": "success",
  "code": 200,
  "data": {
    "items": [...],
    "pagination": {
      "total": 100,
      "page": 1,
      "page_size": 20,
      "total_pages": 5,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

---

## 🧪 Testing Patterns

### Backend Test
```python
from django.test import TestCase
from modules.doccheck.services import DocCheckService

class DocCheckServiceTest(TestCase):
    def test_assess_urban_resident(self):
        session = DocCheckService.start_session(
            email="test@example.com",
            property_type="apartment",
            property_location="Lisbon",
            is_mortgaged=False,
            is_inherited=False
        )
        result = DocCheckService.assess(session.id)
        
        self.assertEqual(result.required_tier, "standard")
        self.assertIn("caderneta", result.missing_documents)
```

### Frontend Test
```typescript
import { render, screen } from '@testing-library/react';
import { OrderForm } from '@/modules/docready/components/OrderForm';

describe('OrderForm', () => {
  it('submits order data', async () => {
    render(<OrderForm />);
    
    const submitButton = screen.getByRole('button', { name: /submit/i });
    expect(submitButton).toBeEnabled();
  });
});
```

---

## 📱 Module Endpoints Summary

| Module | Method | Endpoint | Purpose |
|--------|--------|----------|---------|
| DocCheck | POST | `/api/doccheck/start` | Start assessment |
| DocCheck | GET | `/api/doccheck/{id}/result` | Get results |
| DocReady | POST | `/api/orders` | Create order |
| DocReady | GET | `/api/orders/{id}` | Get order |
| Documents | POST | `/api/documents/{id}/upload` | Upload doc |
| Documents | GET | `/api/documents/{id}` | List docs |
| Payments | POST | `/api/payments/checkout` | Checkout session |
| Payments | GET | `/api/payments/{id}/status` | Payment status |
| SmartCMA | POST | `/api/cma/generate` | Generate report |
| SmartCMA | GET | `/api/cma/{id}` | Get report |
| Operator | GET | `/api/operator/queue` | Get queue |
| Operator | PATCH | `/api/operator/{id}/status` | Update status |

---

## 💾 Database Connection

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fizbo_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🚨 Common Errors & Solutions

**Import Error: `ModuleNotFoundError`**
- Make sure you're importing from `shared`, not relative imports
- Check `PYTHONPATH` includes project root

**API 400 Error: Validation failed**
- Check request data matches serializer fields
- Validate required fields are present
- Check error message in response

**Frontend: Colors not working**
- Use `BRAND_COLORS` from `shared/theme/colors.ts`
- In Tailwind: use `className="bg-primary"` (defined in config)
- In inline: use `style={{ backgroundColor: BRAND_COLORS.primary }}`

**Database migrations**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

---

## 📚 Documentation Files

- **ARCHITECTURE.md** - Full architecture guide
- **modules/** - Diagram files (use case, class, sequence)
- **backend_django/requirements.txt** - Python dependencies
- **frontend_seller_platform/package.json** - Node dependencies

---

**Last Updated**: March 2026
**Status**: ✅ Production Ready
