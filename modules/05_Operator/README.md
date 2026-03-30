# Operator Module

## Overview
The Operator module provides a comprehensive dashboard for Fizbo operators to manage the entire document procurement workflow. It enables queue management, supplier coordination, status updates, and seller communication—all essential for timely order completion.

## Key Features
- **Order Queue**: Real-time dashboard showing all active orders with urgency flags
- **Filtering & Search**: Status, tier, days-open filters; search by order ID, seller, address
- **Order Details**: Complete context including property data, seller info, document checklist
- **Document Status Management**: Update document status with automatic seller notifications
- **Supplier Coordination**: Book peritos, solicitadores, coordinate with municipal offices
- **Seller Actions**: Request specific actions (procuration, upload, signature) with messaging
- **Block Management**: Flag blocked orders with reasons and estimated resolution dates
- **Communications Log**: Complete history of all notifications and messages
- **Real-Time Updates**: Supabase Realtime subscriptions for live queue updates

## Tech Stack
- **Frontend**: React dashboard components with real-time subscriptions
- **Backend**: tRPC operator router with admin auth checks
- **Database**: Supabase `platform_ops.operator_queue` and related tables
- **Real-Time**: Supabase Realtime channel subscriptions
- **Notifications**: Integrated with shared notification service
- **Authentication**: Admin-only access (user_type = "admin")

## Data Model
- `OperatorQueue`: Task queue with priority and assignment
- `OperatorDashboard`: Queue view with filters and sorting
- `OrderManagement`: Document and order status operations
- `SupplierCoordination`: Supplier booking and tracking
- `CommunicationLog`: All notifications and messages sent/received
- `TaskQueue`: Operator's personal task list
- `OperatorMetrics`: Performance KPIs (completion time, satisfaction, etc.)

## Workflows
1. **Queue Review**: Operator opens dashboard → views active orders by urgency
2. **Order Processing**: Click order → view details → update document statuses
3. **Supplier Booking**: Select supplier type → book appointment → track delivery
4. **Seller Requests**: Request action with templated message → automatic notification
5. **Block Management**: Flag blocked order with reason → seller notified
6. **Completion**: Mark order complete → SmartCMA generation triggered → seller notification

## Daily Routine (Operations Manual)
- **08:30**: Review queue sorted by urgency
- **08:45**: Process new orders, confirm document requirements
- **09:00**: Follow up on pending government requests (phone preferred)
- **10:00**: Check perito qualificado confirmations
- **11:00**: Update document statuses (triggers automatic notifications)
- **Afternoon**: Handle seller questions and uploaded documents
- **EOD**: Flag any blocked orders; ensure no order goes 48h without update

## Supplier Management
- **Peritos Qualificados**: Energy certificate specialists (2–4 day turnaround)
- **Solicitadores**: Legal review and conveyancing (fixed-fee packages)
- **Câmaras Municipais**: Municipal offices for Licença Utilização (5–15 day timeline)
- **Administrators**: Condominium declarations (10-day legal response time)

## Performance Metrics
- Average order completion time (target: < 18 working days)
- Orders completed per week
- Customer satisfaction (NPS post-completion)
- Blocked order rate and resolution time
- Document request success rate

## Integration Points
- **Incoming**: Stripe webhook (new orders), Inngest (scheduled tasks)
- **Outgoing**: Notifications (email/WhatsApp), Supplier contacts, Document service
