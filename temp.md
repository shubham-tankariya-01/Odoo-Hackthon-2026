# Backend Work Distribution (3 Members)

## Overview

The backend is divided into **3 business domains**, not by individual files.

Each member owns an entire feature from:
- Controllers
- Services
- Models
- Schemas
- Business Rules
- Tests

This minimizes merge conflicts and keeps responsibilities clear.

---

# Backend Architecture

```
Client
   │
   ▼
Router
   │
   ▼
Controller
   │
   ▼
Service
   │
   ▼
Repository / Store
   │
   ▼
Database / In-Memory Store
```

### Layer Responsibilities

- **Router** → Registers API endpoints
- **Controller** → Handles HTTP request & response
- **Service** → Implements business logic
- **Repository / Store** → Handles data access
- **Models** → Entity definitions
- **Schemas** → Request/Response validation

---

# 👤 Backend Member 1 — Foundation & Organization (Backend Lead)

## Responsibilities

Owns all project infrastructure and organization modules.

### Foundation

- FastAPI setup
- `main.py`
- Config
- Dependencies
- Middleware
- JWT Authentication
- Password Hashing
- Exception Handling
- Shared Response Format

### Authentication

- Signup
- Login
- Logout
- Forgot Password
- Reset Password
- Current User (`/me`)

### Organization

- Departments
- Users / Employees
- Asset Categories

---

## Modules

```
Auth
Departments
Users
Categories
```

---

## Controllers

```
auth_controller.py

department_controller.py

user_controller.py

category_controller.py
```

---

## Services

```
auth_service.py

department_service.py

user_service.py

category_service.py
```

---

## Endpoints

```
/auth

/departments

/categories

/employees
```

---

## Also Responsible For

- Folder structure
- Coding conventions
- Pull request reviews
- Integration
- Shared utilities

---

# 👤 Backend Member 2 — Asset Lifecycle

## Responsibilities

Owns the complete lifecycle of every asset.

Everything related to

- Asset Registration
- Allocation
- Transfers
- Maintenance

belongs here.

---

## Modules

```
Assets

Allocations

Transfers

Maintenance
```

---

## Controllers

```
asset_controller.py

allocation_controller.py

transfer_controller.py

maintenance_controller.py
```

---

## Services

```
asset_service.py

allocation_service.py

transfer_service.py

maintenance_service.py
```

---

## Endpoints

```
/assets

/allocations

/transfers

/maintenance
```

---

## Business Rules

Responsible for implementing

### Asset State Machine

```
Available

↓

Allocated

↓

Returned

↓

Available
```

```
Available

↓

Under Maintenance

↓

Available
```

```
Available

↓

Reserved

↓

Allocated
```

---

Also implements

- Asset allocation
- Return workflow
- Transfer approval
- Maintenance approval
- Asset status updates
- Conflict detection

---

# 👤 Backend Member 3 — Operations & Reporting

## Responsibilities

Owns every operational module after assets exist.

---

## Modules

```
Bookings

Dashboard

Reports

Audits

Notifications

Activity Logs
```

---

## Controllers

```
booking_controller.py

dashboard_controller.py

report_controller.py

audit_controller.py

activity_log_controller.py
```

---

## Services

```
booking_service.py

dashboard_service.py

report_service.py

audit_service.py

activity_log_service.py
```

---

## Endpoints

```
/bookings

/dashboard

/reports

/audits

/activity

/notifications
```

---

## Business Rules

Responsible for

- Booking overlap detection
- Dashboard KPIs
- Audit workflow
- Report generation
- Activity logging
- Notifications

---

# Dependency Flow

```
Authentication
       │
       ▼
Organization
       │
       ▼
Assets
       │
 ┌─────┴────────┐
 ▼              ▼
Allocation   Maintenance
       │
       ▼
Transfer
       │
 ┌─────┴─────────────┐
 ▼                   ▼
Dashboard       Activity Logs
       │
       ▼
Reports

Bookings ─────────────┐
                       │
Audits ────────────────┘
```

---

# Shared Components

Nobody owns these exclusively.

Everyone can contribute when needed.

```
schemas/

models/

constants/

exceptions/

responses/

validators/
```

---

# Coding Rules

Every feature follows the same flow.

```
Router

↓

Controller

↓

Service

↓

Repository

↓

Database
```

### Business Logic Rule

Business logic **must only exist inside Services**.

Controllers should:

- Receive requests
- Validate input
- Call service methods
- Return responses

Repositories should:

- Read data
- Write data

Nothing more.

---

# Git Workflow

Every developer works on their own branch.

```
feature/auth

feature/assets

feature/operations
```

Never commit directly to `main`.

Use Pull Requests for merging.

---

# Integration Responsibility

Backend Lead (Member 1) is responsible for

- Reviewing Pull Requests
- Resolving merge conflicts
- Maintaining architecture consistency
- Verifying coding standards
- Final backend integration

---

# Development Order

## Phase 1

- Project setup
- Authentication
- Assets
- Booking

---

## Phase 2

- Departments
- Categories
- Allocation
- Transfers
- Maintenance

---

## Phase 3

- Dashboard
- Reports
- Activity Logs
- Notifications
- Audits

---

# Goal

Each developer owns a **complete business domain** instead of isolated files.

This allows parallel development while minimizing merge conflicts and making each module independently testable.