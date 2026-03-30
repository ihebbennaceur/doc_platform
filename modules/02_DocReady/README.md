# DocReady Module

## Overview
The DocReady module orchestrates the entire order lifecycle: from tier selection through payment, account creation, property onboarding (via OCR), and workflow initiation.

## Key Features
- **Stripe Integration**: Secure payment processing with VAT handling
- **Automatic Account Creation**: Post-payment account setup with magic link
- **OCR Processing**: Caderneta upload with automatic field extraction
- **Fallback Handling**: Manual entry form if OCR confidence is low
- **Service Tiers**: Standard (€399), Premium (€899), Express (€1,499), Custom
- **Workflow Triggering**: Inngest event emission to start document procurement

## Tech Stack
- **Frontend**: Next.js with tRPC client
- **Backend**: tRPC routers + Next.js API routes
- **Payment**: Stripe Checkout Sessions API + webhooks
- **OCR**: Mistral OCR API (FastAPI service)
- **Workflow**: Inngest cloud functions
- **Database**: Supabase (fizbo_orders, personal_data.seller_profiles, property_intelligence.properties)

## Data Model
- `FizboOrder`: Core order entity with status lifecycle
- `SellerProfile`: Seller details, residency, language, phone
- `Property`: Property metadata from caderneta OCR
- `PaymentSession`: Stripe checkout session tracking
- `ServiceTier`: Pricing and delivery definition
- `CadernetaUpload`: OCR tracking and extracted data

## Workflows
1. **Tier Selection**: User selects from Standard/Premium/Express
2. **Payment**: Stripe Checkout → webhook confirmation
3. **Account Creation**: Auto-created from Stripe session data
4. **Property Onboarding**: Caderneta upload → OCR → confirmation/manual correction
5. **Workflow Initiation**: Inngest event triggers document procurement
6. **Status Tracking**: Real-time updates to seller dashboard

## Refund Policy
- 100% refund if no documents requested within 5 working days
- 50% refund if work started but no docs obtained
- 0% once any document is obtained

## Integration Points
- **Incoming**: From DocCheck (tier recommendation) or direct access
- **Outgoing**: Stripe (payment), Inngest (workflow), Notifications (email/WhatsApp)
