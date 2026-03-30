# DocCheck Module

## Overview
The DocCheck module is the acquisition tool for Fizbo. It's a free, self-serve assessment that helps sellers understand what documents they need to prepare a property for sale.

## Key Features
- **Fast Assessment**: 8 questions completed in under 90 seconds
- **Personalized Results**: Document matrix tailored to property type and seller situation
- **Service Tier Recommendation**: Automatic tier selection (Standard/Premium/Express/Custom)
- **Risk Identification**: Flags problematic scenarios (inherited property, energy class issues, etc.)
- **Session Persistence**: 24-hour browser session for result viewing
- **Lead Capture**: Email collection even without conversion

## Tech Stack
- **Frontend**: Next.js React components
- **Backend**: FastAPI Python service (services/api/doccheck/)
- **Decision Engine**: Rule-based evaluation tree
- **Database**: Supabase `platform_ops.doccheck_sessions`

## Data Model
- `DocCheckSession`: Browser session with answers and results
- `DocCheckAnswers`: 8-question response set
- `DocCheckResult`: Evaluated outcome with documents, tier, price, timeline
- `DocumentRequirement`: Individual document with cost and validity
- `ServiceTier`: Pricing and delivery tier definition

## Workflows
1. **Assessment Flow**: User answers 8 questions → system evaluates → display result
2. **Conversion Flow**: User email captured → result persists → conversion to order

## Key Decisions
- Email required only to view full result (lead capture mechanism)
- 24-hour session expiry (daily cleanup via Inngest cron)
- Price deduction for valid energy cert (-€100 on Standard tier)
- Multiple conditions trigger different tiers (inherited, non-resident, urgent)

## Integration Points
- **Incoming**: User from homepage or PropCheck CTA
- **Outgoing**: Stripe checkout flow (DocReady orders), email notifications
