# SmartCMA Module

## Overview
The SmartCMA module provides sellers with data-backed price intelligence and market insights. It aggregates valuation data from PropCheck, comparable transactions, buyer interest signals, and energy impact analysis to produce a comprehensive price report.

## Key Features
- **Price Band**: Conservative, median, and optimistic price estimates with confidence scoring
- **Comparable Transactions**: 3–5 anonymised comparable properties in same typology/parish (12-month window)
- **Reality Gap**: Municipality-specific asking-to-transaction discount intelligence
- **Days-on-Market Prediction**: Estimated sale timeline at 3 price points
- **BuyerHeat**: Count of verified buyers matching property profile (from Reserva platform)
- **Energy Impact**: Premium/discount estimation based on energy class vs. comparables
- **PDF Export**: Server-side rendered report via @react-pdf/renderer

## Tech Stack
- **Frontend**: React components for report display
- **Backend**: tRPC smartcma router
- **Valuation**: PropCheck AVM (internal API call)
- **Buyer Data**: Reserva platform API
- **PDF Generation**: @react-pdf/renderer (server-side)
- **Storage**: Supabase Storage for PDF files
- **Database**: Supabase `property_intelligence` schema

## Data Model
- `SmartCMAReport`: Main report entity with all sections
- `PriceBand`: Three-point price estimate with confidence
- `Comparable`: Anonymised transaction reference (3–5 per report)
- `RealityGap`: Municipality market dynamics
- `DaysOnMarket`: Timeline predictions at price points
- `BuyerHeat`: Buyer pool availability from Reserva
- `EnergyImpact`: Energy class value adjustment
- `ValuationEngine`: PropCheck integration
- `ReservaAPI`: Buyer pool queries
- `PDFGenerator`: PDF rendering and storage

## Workflows
1. **Report Trigger**: Seller clicks "See my SmartCMA" on completed order dashboard
2. **Data Aggregation**: PropCheck AVM → comparable queries → Reserva buyer lookup
3. **Analysis**: Reality gap + days-on-market + energy impact calculations
4. **PDF Generation**: React PDF template rendering with data
5. **Storage**: PDF uploaded to Supabase, signed URL generated (24-hour expiry)
6. **Notification**: Email sent when report ready for seller

## Performance Targets
- Report generation: < 60 seconds end-to-end
- PDF generation: < 60 seconds
- Fallback: If timeout, email PDF later

## Integration Points
- **Incoming**: DocReady order completion, Seller dashboard
- **Outgoing**: PropCheck (valuation), Reserva (buyers), Supabase Storage (PDF)

## Report Sections
1. Price band (low/mid/high with confidence)
2. Comparable transactions (anonymised table)
3. Reality gap (market discount insight)
4. Days-on-market prediction (3 price scenarios)
5. BuyerHeat (matching buyer count)
6. Energy class impact (premium/discount)
7. CTA: Activate off-market listing on Reserva
