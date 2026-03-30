# Documents Module

## Overview
The Documents module manages the entire document lifecycle: from initial creation as missing, through request, pending, completion, and expiry monitoring. It integrates with Supabase Storage for secure private document storage.

## Key Features
- **Document Tracking**: Status progression (missing → requested → pending → complete → expiring)
- **Secure Storage**: Private Supabase Storage bucket with signed URL access (1-hour expiry)
- **Validity Rules**: Document-specific validity periods and renewal requirements
- **Expiry Monitoring**: Daily cron job checking expiration dates and sending alerts
- **File Uploads**: Seller and operator upload support with OCR verification
- **Signed URLs**: Temporary, secure download links instead of public URLs

## Tech Stack
- **Frontend**: React components with document upload
- **Backend**: tRPC document routers
- **Storage**: Supabase private bucket "fizbo-documents"
- **Database**: Supabase `property_intelligence.fizbo_documents` table
- **Monitoring**: Inngest cron for expiry checks

## Data Model
- `FizboDocument`: Core document entity with status lifecycle
- `DocumentUpload`: File upload tracking and verification
- `DocumentType`: Enum of 8 document types
- `DocumentStatus`: Enum of 6 status states
- `DocumentValidity`: Validity rules and renewal timelines
- `DocumentExpiryMonitor`: Expiry tracking and alert state
- `StorageManager`: Supabase Storage interface

## Document Types & Validity
| Document | Validity | Obtainable By | Cost |
|----------|----------|---------------|------|
| Caderneta Predial | 12 months | Owner | €0 online |
| Certidão Permanente | 6 months | Anyone | €15 online |
| Licença Utilização | No expiry | Procuração | €6–€60 |
| Certificado Energético | 10 years | Perito | €120–€280 |
| Declaração Condomínio | ~30 days | Administrator | €0–€50 |
| Distrate Hipoteca | At escritura | Bank | €0 + €50 reg |
| Habilitação Herdeiros | Permanent | Procuração | €150–€425 |

## Workflows
1. **Operator-Initiated Request**: Operator marks document as requested → system notifies seller
2. **Seller Upload**: Seller uploads file → OCR verification → status pending
3. **Operator Completion**: Operator marks complete → document ready for download
4. **Expiry Monitoring**: Daily check → 30-day warning → 7-day critical alert

## Security
- All documents in private bucket (no public URLs)
- Signed URLs expire after 1 hour
- Access controlled via RLS policies
- No document data in plaintext logs

## Integration Points
- **Incoming**: From DocReady (order creation), Operator actions
- **Outgoing**: Notifications (email/WhatsApp), Storage (Supabase)
