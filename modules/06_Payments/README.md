# Payments Module

## Overview
The Payments module handles all financial transactions in Fizbo. It integrates with Stripe for card processing, calculates personalized pricing with discounts, manages VAT, processes refunds according to policy, and sends payment confirmations.

## Key Features
- **Stripe Integration**: Checkout Sessions API for secure payment processing
- **Dynamic Pricing**: Base price + conditional discounts (energy cert -€100)
- **VAT Handling**: Automatic 23% Portuguese VAT calculation and display
- **Price Breakdown**: Clear itemization at checkout (service + discount + VAT + total)
- **Refund Policy**: Three-tier eligibility (100% / 50% / 0%) based on work progress
- **Webhook Processing**: Secure Stripe event handling with signature verification
- **Payment Notifications**: Confirmation emails and WhatsApp notifications
- **Zero Card Storage**: PCI compliance—no card data stored on Fizbo servers

## Tech Stack
- **Payment Gateway**: Stripe Checkout Sessions API + webhooks
- **Backend**: tRPC routers for session creation
- **Database**: Supabase for payment session and refund tracking
- **Notifications**: Shared notification service (Resend + 360dialog)
- **Security**: Webhook signature verification, encrypted connection

## Data Model
- `PaymentSession`: Checkout session tracking (pending → completed → refunded)
- `PricingCalculator`: Dynamic price computation with discounts
- `PriceBreakdown`: Itemized cost display (service, discount, VAT, total)
- `RefundPolicy`: Refund eligibility rules and calculations
- `RefundEligibility`: Evaluated eligibility for specific order
- `PaymentRefund`: Processed refund transaction tracking
- `StripeWebhookHandler`: Webhook event processor
- `PaymentNotification`: Payment-related notifications

## Pricing Tiers
| Tier | Base Price | Energy Cert Discount | Final (with VAT) | Timeline |
|------|-----------|---------------------|-----------------|----------|
| Standard | €399 | -€100 if applicable | €491–€604 | 15–20 days |
| Premium | €899 | N/A | €1,105 | 20–30 days |
| Express | €1,499 | N/A | €1,843 | 48h start, 10 days |
| Custom | Quote | N/A | Quote | TBD |

## Refund Policy
1. **100% Refund**: If no documents requested within 5 working days
2. **50% Refund**: If work started but no documents obtained
3. **0% Refund**: Once any document is obtained

## Workflows
1. **Checkout Creation**: Calculate price → create Stripe session → display breakdown
2. **Payment**: Seller completes Stripe checkout → system processes charge
3. **Confirmation**: Webhook received → payment confirmed → order created → account created
4. **Refund Request**: Operator evaluates eligibility → Stripe processes refund → notification sent

## Webhook Events Handled
- `checkout.session.completed`: Order created, account activated
- `payment_intent.succeeded`: Payment confirmation
- `payment_intent.failed`: Payment failure notification
- `charge.refunded`: Refund processed notification

## Security
- Stripe webhook signature verification (STRIPE_WEBHOOK_SECRET)
- No card data stored (PCI Level 1 compliance via Stripe)
- VAT-exclusive internal storage, VAT-inclusive user display
- Idempotent payment processing (prevents double-charging)
- Encrypted payment intent IDs in database

## Integration Points
- **Incoming**: DocReady tier selection
- **Outgoing**: Stripe (payment processing), Notifications (email/WhatsApp), Database
