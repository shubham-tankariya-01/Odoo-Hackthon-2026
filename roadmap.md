# AssetFlow Backend Roadmap

## Overall Architecture

```
Client
    │
    ▼
Controllers
    │
    ▼
Services (Business Logic)
    │
    ▼
Repositories
    │
    ▼
Database
```

---

# Modules

1. Authentication
2. Dashboard
3. Organization
4. Assets
5. Allocations
6. Transfers
7. Resource Booking
8. Maintenance
9. Audits
10. Reports
11. Notifications
12. Activity Logs

---

# Folder Structure

```
src/
│
├── controllers/
├── services/
├── repositories/
├── routes/
├── middleware/
├── models/
├── validators/
├── utils/
├── config/
└── app.js
```

---

# Authentication

## Endpoints

### POST /auth/login

Login user.

### POST /auth/logout

Logout current session.

### POST /auth/forgot-password

Request password reset.

### POST /auth/reset-password

Reset password.

### GET /auth/me

Current user profile.

---

# Dashboard

## Endpoints

### GET /dashboard

Returns

- Assets Available
- Assets Allocated
- Maintenance Today
- Active Bookings
- Pending Transfers
- Upcoming Returns
- Overdue Returns

---

# Organization

## Departments

GET /departments

GET /departments/:id

POST /departments

PATCH /departments/:id

DELETE /departments/:id

---

## Asset Categories

GET /categories

POST /categories

PATCH /categories/:id

DELETE /categories/:id

---

## Employees

GET /employees

GET /employees/:id

PATCH /employees/:id

PATCH /employees/:id/promote

PATCH /employees/:id/status

---

# Assets

## CRUD

GET /assets

GET /assets/:id

POST /assets

PATCH /assets/:id

DELETE /assets/:id

---

## Search

GET /assets/search

Query Params

- assetTag
- serial
- category
- department
- location
- status

---

## History

GET /assets/:id/history

Returns

- Allocation History
- Maintenance History

---

## QR

GET /assets/:id/qrcode

---

# Allocation

## Allocate Asset

POST /allocations

---

## View Allocation

GET /allocations

GET /allocations/:id

---

## Return Asset

PATCH /allocations/:id/return

---

## Overdue

GET /allocations/overdue

---

# Transfer Workflow

POST /transfers

GET /transfers

GET /transfers/:id

PATCH /transfers/:id/approve

PATCH /transfers/:id/reject

PATCH /transfers/:id/cancel

---

# Resource Booking

POST /bookings

GET /bookings

GET /bookings/:id

PATCH /bookings/:id

DELETE /bookings/:id

---

## Calendar

GET /bookings/calendar

Query

- resource
- month

---

## Availability

GET /bookings/availability

Query

- resource
- start
- end

---

# Maintenance

POST /maintenance

GET /maintenance

GET /maintenance/:id

PATCH /maintenance/:id/approve

PATCH /maintenance/:id/reject

PATCH /maintenance/:id/assign

PATCH /maintenance/:id/start

PATCH /maintenance/:id/resolve

---

# Audits

POST /audits

GET /audits

GET /audits/:id

PATCH /audits/:id

PATCH /audits/:id/close

---

## Audit Items

POST /audits/:id/items

PATCH /audits/:id/items/:itemId

GET /audits/:id/report

---

# Reports

GET /reports/utilization

GET /reports/maintenance

GET /reports/department

GET /reports/bookings

GET /reports/retirement

GET /reports/export

---

# Notifications

GET /notifications

PATCH /notifications/:id/read

PATCH /notifications/read-all

DELETE /notifications/:id

---

# Activity Logs

GET /activity

GET /activity/:id

Filters

- user
- module
- date
- action

---

# Services

## AuthService

- login()
- logout()
- resetPassword()

---

## DepartmentService

- createDepartment()
- updateDepartment()
- deactivateDepartment()

---

## EmployeeService

- createEmployee()
- promoteEmployee()
- deactivateEmployee()

---

## AssetService

- registerAsset()
- updateAsset()
- searchAssets()
- getHistory()
- updateStatus()

---

## AllocationService

- allocateAsset()
- returnAsset()
- validateAllocation()
- getOverdueAssets()

---

## TransferService

- createTransferRequest()
- approveTransfer()
- rejectTransfer()
- executeTransfer()

---

## BookingService

- createBooking()
- validateOverlap()
- rescheduleBooking()
- cancelBooking()

---

## MaintenanceService

- createRequest()
- approveRequest()
- rejectRequest()
- assignTechnician()
- startMaintenance()
- resolveMaintenance()

---

## AuditService

- createAuditCycle()
- assignAuditors()
- verifyAsset()
- generateDiscrepancyReport()
- closeAudit()

---

## DashboardService

- getKPIs()
- getUpcomingReturns()
- getMaintenanceSummary()

---

## ReportService

- utilizationReport()
- maintenanceReport()
- bookingHeatmap()
- departmentSummary()
- export()

---

## NotificationService

- createNotification()
- markRead()
- sendReminder()

---

## ActivityLogService

- logAction()
- getLogs()

---

# Middleware

Authentication

- verifyJWT()

Authorization

- requireAdmin()
- requireAssetManager()
- requireDepartmentHead()

Validation

- validateRequest()

Error Handling

- globalErrorHandler()

Logging

- requestLogger()

---

# Business Rules

## Asset

- Only Available assets can be allocated.
- Under Maintenance assets cannot be allocated.
- Lost assets cannot be allocated.
- Retired assets cannot be allocated.
- Disposed assets cannot be allocated.

---

## Allocation

- Asset must be Available.
- One active allocation per asset.
- Return changes asset status to Available.
- Overdue allocations trigger notifications.

---

## Transfer

- Asset must already be allocated.
- Cannot transfer returned assets.
- Approval required before transfer.
- Previous allocation closes automatically.

---

## Booking

- No overlapping bookings.
- Cancelled bookings free the slot.
- Reminder before booking starts.

---

## Maintenance

- Approval required.
- Asset status becomes Under Maintenance.
- Resolve changes status to Available.
- History must be preserved.

---

## Audit

- Audit cycles lock after closure.
- Missing assets become Lost.
- Audit history is immutable.

---

# Suggested Development Order

1. Authentication
2. Middleware
3. Organization
4. Asset CRUD
5. Allocation
6. Transfer Workflow
7. Maintenance
8. Booking
9. Dashboard
10. Notifications
11. Reports
12. Audit
13. Activity Logs

---

# Priority for Hackathon

## Must Have

- Authentication
- Asset CRUD
- Allocation
- Transfer
- Maintenance
- Dashboard

## Should Have

- Booking
- Notifications
- Reports

## Nice to Have

- QR Code
- Heatmaps
- Activity Logs
- Audit Cycle
- Export