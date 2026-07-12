# AssetFlow — FastAPI Backend Implementation Plan

## Problem Summary

Build the backend for **AssetFlow**, an Enterprise Asset & Resource Management System. The system lets organizations track, allocate, and maintain physical assets and shared resources via a centralized platform. Key domains: auth, org setup, asset lifecycle, allocation/transfer, resource booking, maintenance workflows, audits, reports, notifications, and activity logs.

This plan covers **backend only** using **Python + FastAPI**.

---

## Tech Stack

| Layer | Choice | Rationale |
|---|---|---|
| Framework | **FastAPI** | Async, auto-docs (Swagger/ReDoc), Pydantic validation |
| Database | **PostgreSQL** | Relational, strong for ERP with complex joins & constraints |
| ORM | **SQLAlchemy 2.0** (async) | Mature, supports complex relationships |
| Migrations | **Alembic** | Standard SQLAlchemy migration tool |
| Auth | **JWT** (python-jose) + **bcrypt** (passlib) | Stateless auth, secure password hashing |
| Validation | **Pydantic v2** | Built into FastAPI, fast, type-safe |
| File Storage | Local filesystem (dev) / S3-compatible (prod) | For asset photos, documents, attachments |
| Task Queue | **None for MVP** (future: Celery/ARQ) | Booking reminders & overdue checks can be cron-based initially |
| Testing | **pytest** + **httpx** (AsyncClient) | Standard FastAPI testing stack |

---

## Project Structure (MVC)

```
M = Models     → SQLAlchemy ORM models (database tables)
V = Views      → Pydantic schemas (request/response shapes)
C = Controllers → FastAPI route handlers (endpoints + business logic)
```

```
backend/
├── alembic/                        # DB migrations
│   ├── versions/
│   └── env.py
├── alembic.ini
│
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app entry, CORS, router registration
│   ├── config.py                   # Settings via pydantic-settings
│   ├── database.py                 # SQLAlchemy engine, session, Base
│   │
│   ├── models/                     # M — SQLAlchemy ORM models (1 file per table)
│   │   ├── __init__.py             # Exports Base + all models
│   │   ├── user.py                 # Users table
│   │   ├── department.py           # Departments table
│   │   ├── asset_category.py       # Asset Categories table
│   │   ├── asset.py                # Assets table
│   │   ├── allocation.py           # Asset Allocations table
│   │   ├── booking.py              # Resource Bookings table
│   │   ├── maintenance.py          # Maintenance Requests table
│   │   ├── audit_cycle.py          # Audit Cycles table
│   │   ├── audit_finding.py        # Audit Findings table
│   │   └── activity_log.py         # Activity Logs table (+ notifications)
│   │
│   ├── views/                      # V — Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── auth.py                 # LoginRequest, SignupRequest, TokenResponse
│   │   ├── user.py                 # UserCreate, UserUpdate, UserResponse
│   │   ├── department.py           # DepartmentCreate, DepartmentUpdate, DepartmentResponse
│   │   ├── asset_category.py       # CategoryCreate, CategoryResponse
│   │   ├── asset.py                # AssetCreate, AssetUpdate, AssetResponse, AssetHistory
│   │   ├── allocation.py           # AllocationCreate, TransferRequest, AllocationResponse
│   │   ├── booking.py              # BookingCreate, BookingUpdate, BookingResponse, CalendarView
│   │   ├── maintenance.py          # MaintenanceCreate, MaintenanceResponse
│   │   ├── audit.py                # AuditCreate, FindingCreate, DiscrepancyReport
│   │   ├── activity_log.py         # ActivityLogResponse, NotificationResponse
│   │   ├── dashboard.py            # DashboardKPIs, OverdueReturn
│   │   └── common.py               # PaginatedResponse, ErrorResponse
│   │
│   ├── controllers/                # C — FastAPI APIRouters (routes + business logic)
│   │   ├── __init__.py
│   │   ├── auth_controller.py      # signup, login, logout, forgot/reset password, me
│   │   ├── dashboard_controller.py # KPI aggregation
│   │   ├── department_controller.py# CRUD + deactivate
│   │   ├── category_controller.py  # CRUD + delete guard
│   │   ├── user_controller.py      # list, detail, update, promote role, toggle status
│   │   ├── asset_controller.py     # CRUD + search + history + QR
│   │   ├── allocation_controller.py# allocate, return, overdue, transfer request/approve/reject
│   │   ├── booking_controller.py   # CRUD + overlap validation + calendar + availability
│   │   ├── maintenance_controller.py # raise, approve, reject, assign, start, resolve
│   │   ├── audit_controller.py     # cycle CRUD + close + findings + discrepancy report
│   │   ├── report_controller.py    # utilization, maintenance, dept, bookings, retirement, export
│   │   └── activity_log_controller.py # logs list/detail + notifications list/read/read-all
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── request_logger.py       # Auto-log all API requests
│   │
│   ├── dependencies/               # FastAPI Depends() functions
│   │   ├── __init__.py
│   │   ├── auth.py                 # get_current_user, require_role()
│   │   └── database.py             # get_db session dependency
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py             # JWT encode/decode, password hashing
│   │   ├── asset_tag.py            # Auto-generate AF-XXXX tags
│   │   ├── qr_generator.py         # QR code generation
│   │   └── exceptions.py           # Custom HTTP exceptions
│   │
│   └── uploads/                    # Local file upload directory (dev)
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_assets.py
│   ├── test_allocations.py
│   ├── test_bookings.py
│   └── ...
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## Database Schema (Key Models)

### Entity Relationship Overview

```mermaid
erDiagram
    USER ||--|| EMPLOYEE : "has profile"
    EMPLOYEE }o--|| DEPARTMENT : "belongs to"
    DEPARTMENT }o--o| DEPARTMENT : "parent"
    DEPARTMENT }o--o| EMPLOYEE : "head"
    ASSET }o--|| ASSET_CATEGORY : "categorized as"
    ASSET ||--o{ ALLOCATION : "allocated via"
    ALLOCATION }o--|| EMPLOYEE : "assigned to"
    ASSET ||--o{ TRANSFER : "transferred via"
    TRANSFER }o--|| EMPLOYEE : "from"
    TRANSFER }o--|| EMPLOYEE : "to"
    ASSET ||--o{ BOOKING : "booked via"
    BOOKING }o--|| EMPLOYEE : "booked by"
    ASSET ||--o{ MAINTENANCE : "maintained via"
    MAINTENANCE }o--|| EMPLOYEE : "raised by"
    MAINTENANCE }o--o| EMPLOYEE : "technician"
    AUDIT ||--o{ AUDIT_ITEM : "contains"
    AUDIT_ITEM }o--|| ASSET : "verifies"
    AUDIT }o--o{ EMPLOYEE : "auditors"
    NOTIFICATION }o--|| EMPLOYEE : "for"
    ACTIVITY_LOG }o--|| EMPLOYEE : "by"
```

### Model Details

#### User
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| email | String (unique) | Login credential |
| hashed_password | String | bcrypt |
| is_active | Boolean | Default true |
| created_at | DateTime | |
| updated_at | DateTime | |

#### Employee
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| user_id | FK → User | One-to-one |
| name | String | |
| email | String | Display email |
| department_id | FK → Department | Nullable |
| role | Enum | `employee`, `department_head`, `asset_manager`, `admin` |
| status | Enum | `active`, `inactive` |
| created_at | DateTime | |

#### Department
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| name | String | |
| head_id | FK → Employee | Nullable |
| parent_id | FK → Department | Self-referential, nullable |
| status | Enum | `active`, `inactive` |
| created_at | DateTime | |

#### AssetCategory
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| name | String | e.g. Electronics, Furniture |
| custom_fields | JSON | Optional category-specific fields |
| created_at | DateTime | |

#### Asset
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| name | String | |
| asset_tag | String (unique) | Auto-generated `AF-XXXX` |
| serial_number | String | Nullable |
| category_id | FK → AssetCategory | |
| acquisition_date | Date | |
| acquisition_cost | Decimal | For reports only |
| condition | String | e.g. New, Good, Fair, Poor |
| location | String | |
| status | Enum | `available`, `allocated`, `reserved`, `under_maintenance`, `lost`, `retired`, `disposed` |
| is_bookable | Boolean | Shared/bookable flag |
| photo_url | String | Nullable |
| documents | JSON | Array of file paths |
| created_at | DateTime | |

#### Allocation
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| asset_id | FK → Asset | |
| employee_id | FK → Employee | |
| department_id | FK → Department | Nullable (allocate to dept) |
| allocated_at | DateTime | |
| expected_return_date | Date | Nullable |
| actual_return_date | DateTime | Nullable (filled on return) |
| return_condition | String | Nullable |
| return_notes | Text | Nullable |
| is_active | Boolean | |
| created_at | DateTime | |

#### Transfer
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| asset_id | FK → Asset | |
| from_employee_id | FK → Employee | |
| to_employee_id | FK → Employee | |
| status | Enum | `requested`, `approved`, `rejected`, `completed`, `cancelled` |
| requested_by_id | FK → Employee | |
| approved_by_id | FK → Employee | Nullable |
| reason | Text | |
| created_at | DateTime | |
| resolved_at | DateTime | Nullable |

#### Booking
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| asset_id | FK → Asset | Must be bookable |
| booked_by_id | FK → Employee | |
| start_time | DateTime | |
| end_time | DateTime | |
| status | Enum | `upcoming`, `ongoing`, `completed`, `cancelled` |
| purpose | Text | Nullable |
| created_at | DateTime | |

#### Maintenance
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| asset_id | FK → Asset | |
| raised_by_id | FK → Employee | |
| description | Text | |
| priority | Enum | `low`, `medium`, `high`, `critical` |
| status | Enum | `pending`, `approved`, `rejected`, `assigned`, `in_progress`, `resolved` |
| approved_by_id | FK → Employee | Nullable |
| technician_id | FK → Employee | Nullable |
| resolution_notes | Text | Nullable |
| photo_url | String | Nullable |
| created_at | DateTime | |
| resolved_at | DateTime | Nullable |

#### Audit / AuditItem
| Column | Type | Notes |
|---|---|---|
| **Audit** | | |
| id | UUID (PK) | |
| name | String | Cycle name |
| scope_type | Enum | `department`, `location` |
| scope_value | String | Dept ID or location name |
| start_date | Date | |
| end_date | Date | |
| status | Enum | `open`, `in_progress`, `closed` |
| created_by_id | FK → Employee | |
| created_at | DateTime | |
| closed_at | DateTime | Nullable |
| **AuditItem** | | |
| id | UUID (PK) | |
| audit_id | FK → Audit | |
| asset_id | FK → Asset | |
| auditor_id | FK → Employee | |
| result | Enum | `pending`, `verified`, `missing`, `damaged` |
| notes | Text | Nullable |
| verified_at | DateTime | Nullable |

#### Notification
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| employee_id | FK → Employee | |
| title | String | |
| message | Text | |
| type | String | e.g. `asset_assigned`, `maintenance_approved`, `overdue_return` |
| is_read | Boolean | Default false |
| reference_id | UUID | Nullable, generic FK to related entity |
| reference_type | String | e.g. `allocation`, `maintenance`, `booking` |
| created_at | DateTime | |

#### ActivityLog
| Column | Type | Notes |
|---|---|---|
| id | UUID (PK) | |
| employee_id | FK → Employee | |
| action | String | e.g. `asset_created`, `allocation_returned` |
| module | String | e.g. `assets`, `allocations` |
| entity_id | UUID | Nullable |
| entity_type | String | |
| details | JSON | Extra metadata |
| created_at | DateTime | |

---

## API Endpoints (FastAPI Routers)

All endpoints are prefixed with `/api/v1`. Each router maps directly to your roadmap.

### 1. Auth (`/api/v1/auth`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| POST | `/signup` | ❌ | — | Create Employee account (role=employee) |
| POST | `/login` | ❌ | — | Returns JWT access + refresh token |
| POST | `/logout` | ✅ | Any | Invalidate session (token blocklist) |
| POST | `/forgot-password` | ❌ | — | Send reset link (email) |
| POST | `/reset-password` | ❌ | — | Reset with token |
| GET | `/me` | ✅ | Any | Current user + employee profile |

### 2. Dashboard (`/api/v1/dashboard`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/` | ✅ | Any | KPI cards: available, allocated, maintenance today, active bookings, pending transfers, upcoming/overdue returns |

### 3. Organization — Departments (`/api/v1/departments`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/` | ✅ | Any | List all departments |
| GET | `/{id}` | ✅ | Any | Department detail |
| POST | `/` | ✅ | Admin | Create department |
| PATCH | `/{id}` | ✅ | Admin | Update department |
| PATCH | `/{id}/deactivate` | ✅ | Admin | Soft-deactivate |

### 4. Organization — Categories (`/api/v1/categories`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/` | ✅ | Any | List categories |
| POST | `/` | ✅ | Admin | Create category |
| PATCH | `/{id}` | ✅ | Admin | Update category |
| DELETE | `/{id}` | ✅ | Admin | Delete category (only if no assets linked) |

### 5. Organization — Employees (`/api/v1/employees`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/` | ✅ | Admin, Manager | List employees (filterable) |
| GET | `/{id}` | ✅ | Any | Employee detail |
| PATCH | `/{id}` | ✅ | Admin | Update employee info |
| PATCH | `/{id}/role` | ✅ | Admin | Promote/change role |
| PATCH | `/{id}/status` | ✅ | Admin | Activate/deactivate |

### 6. Assets (`/api/v1/assets`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/` | ✅ | Any | List/search assets (query params: tag, serial, category, department, location, status) |
| GET | `/{id}` | ✅ | Any | Asset detail |
| POST | `/` | ✅ | Asset Manager | Register new asset (auto-generates tag) |
| PATCH | `/{id}` | ✅ | Asset Manager | Update asset |
| DELETE | `/{id}` | ✅ | Admin | Soft-delete (mark Disposed) |
| GET | `/{id}/history` | ✅ | Any | Allocation + maintenance history |
| GET | `/{id}/qrcode` | ✅ | Any | Generate QR code image |

### 7. Allocations (`/api/v1/allocations`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/` | ✅ | Any | List allocations (filter: active, employee, department) |
| GET | `/{id}` | ✅ | Any | Allocation detail |
| POST | `/` | ✅ | Asset Manager, Dept Head | Allocate asset (conflict check) |
| PATCH | `/{id}/return` | ✅ | Asset Manager | Return asset, capture condition + notes |
| GET | `/overdue` | ✅ | Manager+ | Overdue allocations |

### 8. Transfers (`/api/v1/transfers`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/` | ✅ | Any | List transfers |
| GET | `/{id}` | ✅ | Any | Transfer detail |
| POST | `/` | ✅ | Any | Request transfer |
| PATCH | `/{id}/approve` | ✅ | Manager, Dept Head | Approve transfer → execute re-allocation |
| PATCH | `/{id}/reject` | ✅ | Manager, Dept Head | Reject transfer |
| PATCH | `/{id}/cancel` | ✅ | Requester | Cancel own request |

### 9. Bookings (`/api/v1/bookings`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/` | ✅ | Any | List bookings |
| GET | `/{id}` | ✅ | Any | Booking detail |
| POST | `/` | ✅ | Any | Create booking (overlap validation) |
| PATCH | `/{id}` | ✅ | Booker | Reschedule (re-validate overlaps) |
| DELETE | `/{id}` | ✅ | Booker | Cancel booking |
| GET | `/calendar` | ✅ | Any | Calendar view (query: resource_id, month) |
| GET | `/availability` | ✅ | Any | Check slot availability |

### 10. Maintenance (`/api/v1/maintenance`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/` | ✅ | Any | List requests |
| GET | `/{id}` | ✅ | Any | Request detail |
| POST | `/` | ✅ | Any | Raise maintenance request |
| PATCH | `/{id}/approve` | ✅ | Asset Manager | Approve → asset status = under_maintenance |
| PATCH | `/{id}/reject` | ✅ | Asset Manager | Reject request |
| PATCH | `/{id}/assign` | ✅ | Asset Manager | Assign technician |
| PATCH | `/{id}/start` | ✅ | Technician | Mark in-progress |
| PATCH | `/{id}/resolve` | ✅ | Technician | Resolve → asset status = available |

### 11. Audits (`/api/v1/audits`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/` | ✅ | Admin, Manager | List audit cycles |
| GET | `/{id}` | ✅ | Admin, Manager | Audit detail |
| POST | `/` | ✅ | Admin | Create audit cycle + assign auditors |
| PATCH | `/{id}` | ✅ | Admin | Update cycle metadata |
| PATCH | `/{id}/close` | ✅ | Admin | Close cycle → lock, update asset statuses |
| POST | `/{id}/items` | ✅ | Auditor | Submit verification result for an asset |
| PATCH | `/{id}/items/{item_id}` | ✅ | Auditor | Update verification result |
| GET | `/{id}/report` | ✅ | Admin, Manager | Auto-generated discrepancy report |

### 12. Reports (`/api/v1/reports`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/utilization` | ✅ | Manager+ | Asset utilization trends |
| GET | `/maintenance` | ✅ | Manager+ | Maintenance frequency by asset/category |
| GET | `/departments` | ✅ | Manager+ | Department-wise allocation summary |
| GET | `/bookings` | ✅ | Manager+ | Booking heatmap data |
| GET | `/retirement` | ✅ | Manager+ | Assets nearing retirement |
| GET | `/export` | ✅ | Manager+ | Export report as CSV/PDF |

### 13. Notifications (`/api/v1/notifications`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/` | ✅ | Any | User's notifications |
| PATCH | `/{id}/read` | ✅ | Owner | Mark as read |
| PATCH | `/read-all` | ✅ | Owner | Mark all as read |
| DELETE | `/{id}` | ✅ | Owner | Delete notification |

### 14. Activity Logs (`/api/v1/activity`)

| Method | Path | Auth | Role | Description |
|---|---|---|---|---|
| GET | `/` | ✅ | Admin | List logs (filter: user, module, date, action) |
| GET | `/{id}` | ✅ | Admin | Log detail |

---

## Key Business Rules (Enforced in Services)

### Asset Status State Machine

```mermaid
stateDiagram-v2
    [*] --> Available : registered
    Available --> Allocated : allocated
    Available --> Reserved : reserved
    Available --> Under_Maintenance : maintenance approved
    Allocated --> Available : returned
    Allocated --> Under_Maintenance : maintenance approved
    Reserved --> Available : reservation cancelled
    Reserved --> Allocated : reservation fulfilled
    Under_Maintenance --> Available : maintenance resolved
    Available --> Lost : audit flagged missing
    Allocated --> Lost : audit flagged missing
    Available --> Retired : admin retires
    Available --> Disposed : admin disposes
    Retired --> Disposed : admin disposes
```

### Allocation Rules
- Asset **must** be `available` to allocate
- **One active allocation per asset** — if already allocated, block and show current holder + offer transfer request
- Return sets asset status back to `available`
- Overdue allocations (past `expected_return_date`) auto-flagged, feed dashboard + notifications

### Transfer Rules
- Asset **must** already be allocated to someone
- Approval required from Asset Manager or Department Head before re-allocation
- On approval: previous allocation closes automatically, new allocation created, history updated

### Booking Rules
- Asset must have `is_bookable = true`
- **No overlapping time slots** for the same resource — validate `start_time < existing_end_time AND end_time > existing_start_time`
- Cancelled bookings free the slot immediately
- Booking status auto-transitions: `upcoming` → `ongoing` → `completed`

### Maintenance Rules
- Approval required before work begins
- On approval: asset status → `under_maintenance`
- On resolution: asset status → `available`
- Full maintenance history preserved per asset

### Audit Rules
- Audit cycles are **immutable after closure** (locked)
- Assets marked `missing` during audit → status becomes `lost`
- Discrepancy report auto-generated from flagged items

---

## Auth & Security Design

### JWT Flow
1. **Signup** → creates `User` + `Employee` (role = `employee`) → no role self-selection
2. **Login** → validates credentials → returns `access_token` (short-lived, 30min) + `refresh_token` (long-lived, 7d)
3. **Protected routes** → `Authorization: Bearer <token>` → `get_current_user` dependency decodes JWT, loads employee
4. **Role checks** → `require_role(["admin", "asset_manager"])` dependency ensures role authorization

### Role Promotion
- Only via `PATCH /employees/{id}/role` by Admin
- No role selection at signup — this is critical per the PS

### Password Security
- bcrypt hashing via `passlib`
- Forgot password → generates time-limited reset token → sent via email (or returned in dev mode)

---

## Cross-Cutting Concerns

### Notification Generation
Every business action that matters triggers a notification:
- **AllocationService** → `asset_assigned`, `overdue_return`
- **TransferService** → `transfer_requested`, `transfer_approved`, `transfer_rejected`
- **MaintenanceService** → `maintenance_approved`, `maintenance_rejected`, `maintenance_resolved`
- **BookingService** → `booking_confirmed`, `booking_cancelled`, `booking_reminder`
- **AuditService** → `audit_discrepancy_flagged`

### Activity Logging
The `ActivityLogService.log_action()` is called from every service method to record who did what and when. Middleware can also auto-log requests.

### Error Handling
- Custom exception classes in `utils/exceptions.py` (e.g. `AssetNotAvailableError`, `BookingOverlapError`, `TransferNotAllowedError`)
- Global exception handler middleware converts these to proper HTTP responses with structured error bodies

### Pagination
- All list endpoints support `?page=1&page_size=20` with consistent response format:
  ```json
  { "items": [...], "total": 100, "page": 1, "page_size": 20, "pages": 5 }
  ```

---

## Proposed Changes

### Backend Foundation

#### [NEW] [requirements.txt](file:///e:/Coding/Hackthon_Projects/Odoo-Hackthon-2026/backend/requirements.txt)
Core dependencies: `fastapi`, `uvicorn[standard]`, `sqlalchemy[asyncio]`, `asyncpg`, `alembic`, `pydantic-settings`, `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`, `qrcode[pil]`, `httpx`, `pytest`, `pytest-asyncio`.

#### [NEW] [.env.example](file:///e:/Coding/Hackthon_Projects/Odoo-Hackthon-2026/backend/.env.example)
Template for environment variables: `DATABASE_URL`, `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, etc.

#### [NEW] [main.py](file:///e:/Coding/Hackthon_Projects/Odoo-Hackthon-2026/backend/app/main.py)
FastAPI app initialization, CORS middleware, controller registration, global exception handlers.

#### [NEW] [config.py](file:///e:/Coding/Hackthon_Projects/Odoo-Hackthon-2026/backend/app/config.py)
`pydantic-settings` based configuration loading from `.env`.

#### [NEW] [database.py](file:///e:/Coding/Hackthon_Projects/Odoo-Hackthon-2026/backend/app/database.py)
Async SQLAlchemy engine + `AsyncSession` factory + `Base` declarative class.

---

### M — Models Layer (10 files)
SQLAlchemy ORM models mapping directly to the 10 PostgreSQL tables from `schema.md`. Each model defines columns, relationships, and constraints. All models inherit from a shared `Base`.

### V — Views Layer (12 files)
Pydantic v2 schemas for request validation and response serialization. Each module has `Create`, `Update`, and `Response` variants. `common.py` provides shared `PaginatedResponse` and `ErrorResponse` schemas.

### C — Controllers Layer (12 files)
FastAPI `APIRouter` handlers that contain **both** route definitions and business logic. Each controller:
- Receives validated request via Pydantic schemas (Views)
- Queries/mutates the database via SQLAlchemy models (Models)
- Applies business rules (conflict checks, state machine transitions, overlap validation)
- Returns structured responses via Pydantic schemas (Views)
- Uses `Depends(require_role(...))` for role-based access

### Dependencies & Middleware
- `dependencies/auth.py` — `get_current_user`, `require_role`
- `dependencies/database.py` — `get_db` async session
- `middleware/request_logger.py` — auto-log all API requests

### Utilities
- `utils/security.py` — JWT + bcrypt helpers
- `utils/asset_tag.py` — Auto-increment `AF-XXXX` tag generator
- `utils/qr_generator.py` — QR code generation for assets
- `utils/exceptions.py` — Custom exception classes

---

## Development Order (Aligned with Roadmap Priority)

### Phase 1 — Foundation (Must Have)
1. Project setup: `requirements.txt`, `.env`, `config.py`, `database.py`, `main.py`
2. SQLAlchemy models + Alembic initial migration
3. Auth controller (signup, login, JWT, me)
4. Dependencies & middleware (auth, role-check, DB session)
5. Organization controllers (departments, categories, users, role promotion)
6. Asset controller (CRUD + search + auto-tag generation)
7. Allocation controller (allocate, return, conflict blocking, overdue, transfer workflow)
8. Maintenance controller (raise → approve → assign → start → resolve)
9. Dashboard controller (KPIs)

### Phase 2 — Should Have
10. Booking controller (create, overlap validation, calendar, availability)
11. Activity log controller (notifications list/read + admin audit trail)
12. Report controller (utilization, maintenance, department, booking heatmap)

### Phase 3 — Nice to Have
13. QR code generation
14. Audit controller (cycles, findings, close, discrepancy report)
15. Report export (CSV/PDF)

---

## Verification Plan

### Automated Tests
```bash
cd backend
pytest tests/ -v --asyncio-mode=auto
```
- Unit tests for each service (business rule enforcement)
- Integration tests for each router (end-to-end API flow)
- Specific tests for conflict scenarios: double allocation, booking overlap, invalid state transitions

### Manual Verification
- Swagger UI at `http://localhost:8000/docs` — test all endpoints interactively
- Verify role-based access: signup as employee → try admin endpoints → expect 403
- Verify asset state machine: allocate → try re-allocate → expect conflict error
- Verify booking overlap: book 9:00–10:00 → try 9:30–10:30 → expect rejection

> [!IMPORTANT]
> **Email for forgot-password**: Should we implement actual email sending (needs SMTP config) or just return the reset token in the API response for hackathon purposes?

> [!IMPORTANT]
> **File uploads**: For asset photos/documents — should we implement local filesystem storage for now, or skip file uploads entirely and just store URL strings?
