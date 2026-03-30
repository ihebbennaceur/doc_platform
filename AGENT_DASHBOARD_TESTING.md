# Agent Dashboard - Quick Start Guide 🚀

## How to Test the Agent Dashboard

### Step 1: Access the Agent Dashboard

**URL**: `http://localhost:3000/agent/dashboard`

### Step 2: Login as an Agent

To access the agent dashboard, you need to:

1. Set your user role to `'agent'` in localStorage (for testing)
2. You can do this in browser DevTools:
   ```javascript
   // In browser console:
   let user = JSON.parse(localStorage.getItem('user'));
   user.role = 'agent';
   localStorage.setItem('user', JSON.stringify(user));
   
   // Then reload the page
   location.reload();
   ```

3. Or modify the mock data in `/app/agent/dashboard/page.tsx` if testing locally

### Step 3: View Assigned Cases

Once logged in as an agent, you'll see:

- **Case 1**: `dc_case_001`
  - 3 documents (Caderneta, Certidão, Energy Certificate)
  - All documents in "uploaded" status

- **Case 2**: `dc_case_002`
  - 1 document (Caderneta)
  - Document in "pending" status

### Step 4: Verify or Reject Documents

1. Click on any case card to expand it
2. For each document, you'll see:
   - Document icon (📚, 🏛️, ⚡)
   - Document name and key
   - Current status (Pending, Uploaded, Verified, Rejected, Expired)
   - Two action buttons: **✅ Verify Document** and **❌ Reject Document**

3. Click **"✅ Verify Document"** to:
   - Change status to "Verified" (green badge)
   - Create a notification
   - Show success message

4. Click **"❌ Reject Document"** to:
   - Show a text field for rejection reason
   - Change status to "Rejected" (red badge)
   - Include rejection reason in notification
   - Show success message

### Step 5: Check Notifications

In the dashboard header (top right), you'll see:

- **Bell icon 🔔** with a red badge showing unread count
- Click the bell to see all notifications
- Each notification shows:
  - Title: "Document status changed"
  - Message: Document name + new status + rejection reason (if applicable)
  - Timestamp
  - Notification type (verified=green, rejected=red, status_changed=blue)

### Step 6: Test Route Protection

Try accessing `/agent/dashboard` with different roles:

- **As User**: You'll be redirected to `/dashboard`
- **As Agent**: You'll see the agent dashboard
- **As Admin**: You'll be redirected to `/dashboard` (requires role='agent')

## Features to Test

### ✅ Verify Document
```
Click: ✅ Verify Document
Result: 
  - Status badge changes from blue to green
  - Notification created: "Caderneta Informática (2024-2025) - Verified"
  - Success alert appears
  - Status button becomes disabled until page reload
```

### ❌ Reject Document  
```
Click: ❌ Reject Document
Input: "Document appears to be expired"
Result:
  - Status badge changes from blue to red
  - Rejection note field appears
  - Notification created: "Caderneta Informática (2024-2025) - Rejected: Document appears to be expired"
  - Success alert appears
  - Red box with rejection reason displays
```

### 🔔 Notifications
```
After status change:
  - Bell icon unread count increases
  - Click bell to expand dropdown
  - Notification appears in list
  - Auto-hides after 5 seconds (can be marked as read before)
  - Mark as read by clicking on notification
  - Close button to remove notification
```

### 🌐 Language Switching
```
Click: LanguageSwitcher (top right)
Switch to: Portuguese
Result:
  - All text changes to Portuguese
  - "Painel do Agente" instead of "Agent Dashboard"
  - "Verificar Documento" instead of "Verify Document"
  - Notifications in Portuguese
```

### ← Back Navigation
```
From Case Details:
  - Click "← Back to Agent Dashboard"
  - Returns to case list view
  - Can select another case
```

## Testing Checklist

### Functionality ✓
- [ ] Can access `/agent/dashboard` as agent
- [ ] Cannot access `/agent/dashboard` as user (redirects)
- [ ] Case list displays with cards
- [ ] Click case → expands to documents
- [ ] Click document → shows verify/reject buttons
- [ ] Verify button works → status changes to verified
- [ ] Reject button works → status changes to rejected
- [ ] Rejection note appears when rejecting
- [ ] Back button returns to cases list

### Notifications ✓
- [ ] Status change creates notification
- [ ] Bell icon shows unread count
- [ ] Click bell → dropdown opens
- [ ] Notification appears in dropdown
- [ ] Notification includes document name + new status
- [ ] Click notification → marks as read
- [ ] Notification auto-hides after 5 seconds
- [ ] Close button removes notification

### Localization ✓
- [ ] Portuguese translations load correctly
- [ ] English translations load correctly
- [ ] All UI text translates
- [ ] Notification messages translate

### UI/UX ✓
- [ ] Case cards have hover effect (lift animation)
- [ ] Status buttons show loading state
- [ ] Success alert appears after status change
- [ ] Colors match design system
- [ ] Layout responsive on mobile
- [ ] Icons display correctly

### Security ✓
- [ ] Cannot access agent dashboard with user role
- [ ] Cannot access agent dashboard without authentication
- [ ] Route protection works on page load
- [ ] No personal user data visible (case ID only)

## Mock Data

### Case 1: dc_case_001
```
Status: Active
Documents:
  1. Caderneta Informática (2024-2025)
     - Status: Uploaded
     - Uploaded: 7 days ago
     - Expires: 1 year from now
  
  2. Certidão de Propriedade - Imóvel Lisboa
     - Status: Uploaded
     - Uploaded: 2 days ago
     - Expires: 180 days from now
  
  3. Certificado Energético - Loja Porto
     - Status: Uploaded
     - Uploaded: 1 day ago
     - Expires: 90 days from now
```

### Case 2: dc_case_002
```
Status: Active
Documents:
  1. Caderneta Informática (2024-2025)
     - Status: Pending
     - Not yet uploaded
```

## File Structure

```
frontend_seller_platform/src/
├── app/
│   ├── dashboard/
│   │   └── page.tsx (user dashboard with NotificationsCenter)
│   ├── agent/
│   │   └── dashboard/
│   │       └── page.tsx (NEW - agent dashboard)
│   └── ...
├── components/
│   ├── ProtectedRoute.tsx (UPDATED - role checking)
│   ├── NotificationsCenter.tsx (NEW - bell icon + dropdown)
│   ├── LanguageSwitcher.tsx
│   └── ...
├── shared/
│   ├── context/
│   │   ├── LanguageContext.tsx (translations)
│   │   ├── NotificationContext.tsx (NEW - notification state)
│   │   └── ...
│   └── ...
└── ...
```

## API Endpoints (When Ready)

These endpoints are currently mocked but should be implemented in backend:

1. **GET /api/cases/assigned**
   - Returns list of cases assigned to agent
   - Currently: Returns mock data

2. **PATCH /api/cases/{caseId}/documents/{docId}/status**
   - Updates document status
   - Currently: Mock 500ms delay

3. **POST /api/notifications** (Optional)
   - Creates notification for user
   - Currently: Stored in frontend NotificationContext only

## Known Limitations (Current Version)

- ⚠️ All data is mock (frontend only)
- ⚠️ Status changes not persisted to backend
- ⚠️ Notifications not persisted (lost on page reload)
- ⚠️ Case assignment not fetched from backend

## Next Steps

1. **Backend Integration**
   - Create GET /api/cases/assigned endpoint
   - Create PATCH /api/cases/{caseId}/documents/{docId}/status endpoint
   - Update agent dashboard to use real API

2. **Notification Delivery**
   - Send notification to user when status changes
   - Implement webhook or WebSocket for real-time updates

3. **Persistent Storage**
   - Store notifications in database
   - Retrieve on page load

4. **Enhanced Features**
   - Add filters by status
   - Add search by case ID
   - Add pagination for many cases
   - Add export/report functionality

---

**Last Updated**: March 27, 2026
**Version**: 1.0
**Status**: Ready for Testing ✅
