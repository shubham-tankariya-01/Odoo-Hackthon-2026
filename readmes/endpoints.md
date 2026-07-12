# AssetFlow — API Endpoints Reference

Base URL: `/api/v1`

Database: **PostgreSQL** | Auth: **JWT Bearer Token**

---

## Table of Contents

1. [Authentication](#1-authentication)
2. [Dashboard](#2-dashboard)
3. [Departments](#3-departments)
4. [Asset Categories](#4-asset-categories)
5. [Users / Employee Directory](#5-users--employee-directory)
6. [Assets](#6-assets)
7. [Asset Allocations](#7-asset-allocations)
8. [Resource Bookings](#8-resource-bookings)
9. [Maintenance Requests](#9-maintenance-requests)
10. [Audit Cycles](#10-audit-cycles)
11. [Audit Findings](#11-audit-findings)
12. [Activity Logs & Notifications](#12-activity-logs--notifications)
13. [Reports](#13-reports)

---

# 1. Authentication

> Signup always creates an **Employee** role. Roles are assigned only by Admin via the Employee Directory.

---

### `POST /api/v1/auth/signup`

Create a new employee account. Role is always `employee` — no self-elevation.

**Auth:** ❌ None

```json
// Request
{
  "name": "Priya Sharma",
  "email": "priya@company.com",
  "password": "SecurePass123!"
}
```

```json
// Response 201
{
  "id": "a1b2c3d4-...",
  "name": "Priya Sharma",
  "email": "priya@company.com",
  "role": "employee",
  "status": "active",
  "message": "Account created successfully"
}
```

---

### `POST /api/v1/auth/login`

Authenticate and receive JWT tokens.

**Auth:** ❌ None

```json
// Request
{
  "email": "priya@company.com",
  "password": "SecurePass123!"
}
```

```json
// Response 200
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "a1b2c3d4-...",
    "name": "Priya Sharma",
    "email": "priya@company.com",
    "role": "employee",
    "department_id": null
  }
}
```

---

### `POST /api/v1/auth/logout`

Invalidate the current session token.

**Auth:** ✅ Any role

```
Headers: Authorization: Bearer <access_token>
```

```json
// Response 200
{
  "message": "Logged out successfully"
}
```

---

### `POST /api/v1/auth/forgot-password`

Request a password reset token. Token is returned in response for hackathon (email in production).

**Auth:** ❌ None

```json
// Request
{
  "email": "priya@company.com"
}
```

```json
// Response 200
{
  "message": "Password reset token generated",
  "reset_token": "abc123def456..."
}
```

---

### `POST /api/v1/auth/reset-password`

Reset password using the token from forgot-password.

**Auth:** ❌ None

```json
// Request
{
  "token": "abc123def456...",
  "new_password": "NewSecurePass456!"
}
```

```json
// Response 200
{
  "message": "Password reset successfully"
}
```

---

### `GET /api/v1/auth/me`

Get the currently authenticated user's profile.

**Auth:** ✅ Any role

```json
// Response 200
{
  "id": "a1b2c3d4-...",
  "name": "Priya Sharma",
  "email": "priya@company.com",
  "role": "employee",
  "status": "active",
  "department_id": "d5e6f7a8-...",
  "department_name": "Engineering",
  "promoted_by": null
}
```

---

# 2. Dashboard

> Returns KPI data for the authenticated user's operational snapshot.

---

### `GET /api/v1/dashboard`

Returns real-time KPI cards and overdue/upcoming items.

**Auth:** ✅ Any role

```json
// Response 200
{
  "kpis": {
    "assets_available": 42,
    "assets_allocated": 78,
    "maintenance_today": 3,
    "active_bookings": 12,
    "pending_transfers": 5,
    "upcoming_returns": 8,
    "overdue_returns": 2
  },
  "overdue_returns": [
    {
      "allocation_id": "al-001...",
      "asset_tag": "AF-0114",
      "asset_name": "Laptop Dell XPS",
      "employee_name": "Raj Patel",
      "expected_return_date": "2026-07-01",
      "days_overdue": 11
    }
  ],
  "upcoming_returns": [
    {
      "allocation_id": "al-002...",
      "asset_tag": "AF-0032",
      "asset_name": "Projector Epson",
      "employee_name": "Priya Sharma",
      "expected_return_date": "2026-07-15",
      "days_until_due": 3
    }
  ]
}
```

---

# 3. Departments

> Admin-only management. All users can read.

---

### `GET /api/v1/departments`

List all departments with optional filters.

**Auth:** ✅ Any role

**Query Params:** `?status=active&page=1&page_size=20`

```json
// Response 200
{
  "items": [
    {
      "id": "d5e6f7a8-...",
      "name": "Engineering",
      "parent_department_id": null,
      "head_user_id": "u-head-001...",
      "head_name": "Amit Kumar",
      "status": "active"
    },
    {
      "id": "d9a8b7c6-...",
      "name": "Frontend Team",
      "parent_department_id": "d5e6f7a8-...",
      "head_user_id": "u-head-002...",
      "head_name": "Sneha Roy",
      "status": "active"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

### `GET /api/v1/departments/{id}`

Get a single department with its hierarchy and member count.

**Auth:** ✅ Any role

```json
// Response 200
{
  "id": "d5e6f7a8-...",
  "name": "Engineering",
  "parent_department_id": null,
  "head_user_id": "u-head-001...",
  "head_name": "Amit Kumar",
  "status": "active",
  "child_departments": [
    { "id": "d9a8b7c6-...", "name": "Frontend Team" },
    { "id": "dab1c2d3-...", "name": "Backend Team" }
  ],
  "member_count": 24
}
```

---

### `POST /api/v1/departments`

Create a new department.

**Auth:** ✅ Admin only

```json
// Request
{
  "name": "Design Team",
  "parent_department_id": "d5e6f7a8-...",
  "head_user_id": "u-head-003...",
  "status": "active"
}
```

```json
// Response 201
{
  "id": "d-new-001...",
  "name": "Design Team",
  "parent_department_id": "d5e6f7a8-...",
  "head_user_id": "u-head-003...",
  "status": "active"
}
```

---

### `PATCH /api/v1/departments/{id}`

Update department info (name, head, parent, status).

**Auth:** ✅ Admin only

```json
// Request (partial update — send only changed fields)
{
  "head_user_id": "u-head-004...",
  "status": "inactive"
}
```

```json
// Response 200
{
  "id": "d-new-001...",
  "name": "Design Team",
  "parent_department_id": "d5e6f7a8-...",
  "head_user_id": "u-head-004...",
  "status": "inactive"
}
```

---

# 4. Asset Categories

> Admin manages. All users can list.

---

### `GET /api/v1/categories`

List all asset categories.

**Auth:** ✅ Any role

```json
// Response 200
{
  "items": [
    {
      "id": "cat-001...",
      "name": "Electronics",
      "field_schema": {
        "warranty_period_months": "integer",
        "processor": "string"
      }
    },
    {
      "id": "cat-002...",
      "name": "Furniture",
      "field_schema": {
        "material": "string",
        "weight_kg": "number"
      }
    },
    {
      "id": "cat-003...",
      "name": "Vehicles",
      "field_schema": {
        "registration_number": "string",
        "fuel_type": "string"
      }
    }
  ],
  "total": 3,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

### `POST /api/v1/categories`

Create a new asset category with optional custom field schema.

**Auth:** ✅ Admin only

```json
// Request
{
  "name": "Medical Equipment",
  "field_schema": {
    "calibration_date": "date",
    "certification_number": "string"
  }
}
```

```json
// Response 201
{
  "id": "cat-004...",
  "name": "Medical Equipment",
  "field_schema": {
    "calibration_date": "date",
    "certification_number": "string"
  }
}
```

---

### `PATCH /api/v1/categories/{id}`

Update a category.

**Auth:** ✅ Admin only

```json
// Request
{
  "name": "Medical & Lab Equipment"
}
```

```json
// Response 200
{
  "id": "cat-004...",
  "name": "Medical & Lab Equipment",
  "field_schema": {
    "calibration_date": "date",
    "certification_number": "string"
  }
}
```

---

### `DELETE /api/v1/categories/{id}`

Delete a category. **Fails if any assets are linked to it.**

**Auth:** ✅ Admin only

```json
// Response 200
{
  "message": "Category deleted successfully"
}
```

```json
// Error 409
{
  "detail": "Cannot delete category: 12 assets are still linked to 'Electronics'"
}
```

---

# 5. Users / Employee Directory

> Signup creates users. Admin promotes roles here — the **only** place roles are assigned.

---

### `GET /api/v1/users`

List all users/employees. Filterable.

**Auth:** ✅ Admin, Asset Manager

**Query Params:** `?department_id=...&role=employee&status=active&search=priya&page=1&page_size=20`

```json
// Response 200
{
  "items": [
    {
      "id": "a1b2c3d4-...",
      "name": "Priya Sharma",
      "email": "priya@company.com",
      "role": "employee",
      "department_id": "d5e6f7a8-...",
      "department_name": "Engineering",
      "status": "active",
      "promoted_by": null
    },
    {
      "id": "b2c3d4e5-...",
      "name": "Amit Kumar",
      "email": "amit@company.com",
      "role": "department_head",
      "department_id": "d5e6f7a8-...",
      "department_name": "Engineering",
      "status": "active",
      "promoted_by": "admin-001..."
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

### `GET /api/v1/users/{id}`

Get single user/employee detail.

**Auth:** ✅ Any role

```json
// Response 200
{
  "id": "a1b2c3d4-...",
  "name": "Priya Sharma",
  "email": "priya@company.com",
  "role": "employee",
  "department_id": "d5e6f7a8-...",
  "department_name": "Engineering",
  "status": "active",
  "promoted_by": null,
  "allocated_assets_count": 2,
  "active_bookings_count": 1
}
```

---

### `PATCH /api/v1/users/{id}`

Update user info (name, department).

**Auth:** ✅ Admin only

```json
// Request
{
  "name": "Priya S. Sharma",
  "department_id": "d9a8b7c6-..."
}
```

```json
// Response 200
{
  "id": "a1b2c3d4-...",
  "name": "Priya S. Sharma",
  "email": "priya@company.com",
  "role": "employee",
  "department_id": "d9a8b7c6-...",
  "status": "active"
}
```

---

### `PATCH /api/v1/users/{id}/role`

**Promote or change a user's role.** This is the only way to assign roles (Admin, Department Head, Asset Manager). Records who promoted them.

**Auth:** ✅ Admin only

```json
// Request
{
  "role": "asset_manager"
}
```

```json
// Response 200
{
  "id": "a1b2c3d4-...",
  "name": "Priya Sharma",
  "role": "asset_manager",
  "promoted_by": "admin-001...",
  "message": "Role updated to asset_manager"
}
```

**Valid roles:** `employee`, `department_head`, `asset_manager`, `admin`

---

### `PATCH /api/v1/users/{id}/status`

Activate or deactivate a user.

**Auth:** ✅ Admin only

```json
// Request
{
  "status": "inactive"
}
```

```json
// Response 200
{
  "id": "a1b2c3d4-...",
  "name": "Priya Sharma",
  "status": "inactive",
  "message": "User deactivated"
}
```

---

# 6. Assets

> Asset Manager registers/updates. All users can view/search.

---

### `GET /api/v1/assets`

List and search assets. Supports multiple filters.

**Auth:** ✅ Any role

**Query Params:** `?asset_tag=AF-0001&serial_number=...&category_id=...&current_status=available&is_bookable=true&search=laptop&page=1&page_size=20`

```json
// Response 200
{
  "items": [
    {
      "id": "ast-001...",
      "asset_tag": "AF-0001",
      "name": "MacBook Pro 16\"",
      "serial_number": "C02ZW1XXMD6T",
      "category_id": "cat-001...",
      "category_name": "Electronics",
      "current_status": "available",
      "is_bookable": false,
      "custom_fields": {
        "warranty_period_months": 24,
        "processor": "M3 Pro"
      }
    },
    {
      "id": "ast-002...",
      "asset_tag": "AF-0002",
      "name": "Conference Room B2 Projector",
      "serial_number": "EPSON-9912",
      "category_id": "cat-001...",
      "category_name": "Electronics",
      "current_status": "available",
      "is_bookable": true,
      "custom_fields": {
        "warranty_period_months": 12
      }
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

### `GET /api/v1/assets/{id}`

Full asset detail including current holder info.

**Auth:** ✅ Any role

```json
// Response 200
{
  "id": "ast-001...",
  "asset_tag": "AF-0001",
  "name": "MacBook Pro 16\"",
  "serial_number": "C02ZW1XXMD6T",
  "category_id": "cat-001...",
  "category_name": "Electronics",
  "current_status": "allocated",
  "is_bookable": false,
  "custom_fields": {
    "warranty_period_months": 24,
    "processor": "M3 Pro"
  },
  "current_holder": {
    "allocation_id": "al-001...",
    "employee_id": "a1b2c3d4-...",
    "employee_name": "Priya Sharma",
    "department_name": "Engineering",
    "allocated_at": "2026-06-15T10:00:00Z",
    "expected_return_date": "2026-12-15"
  }
}
```

---

### `POST /api/v1/assets`

Register a new asset. `asset_tag` is auto-generated (AF-XXXX). Status defaults to `available`.

**Auth:** ✅ Asset Manager

```json
// Request
{
  "name": "Dell Monitor 27\"",
  "serial_number": "DELL-U2723QE-001",
  "category_id": "cat-001...",
  "is_bookable": false,
  "custom_fields": {
    "warranty_period_months": 36
  }
}
```

```json
// Response 201
{
  "id": "ast-003...",
  "asset_tag": "AF-0003",
  "name": "Dell Monitor 27\"",
  "serial_number": "DELL-U2723QE-001",
  "category_id": "cat-001...",
  "category_name": "Electronics",
  "current_status": "available",
  "is_bookable": false,
  "custom_fields": {
    "warranty_period_months": 36
  }
}
```

---

### `PATCH /api/v1/assets/{id}`

Update asset details.

**Auth:** ✅ Asset Manager

```json
// Request
{
  "name": "Dell UltraSharp Monitor 27\"",
  "is_bookable": true
}
```

```json
// Response 200
{
  "id": "ast-003...",
  "asset_tag": "AF-0003",
  "name": "Dell UltraSharp Monitor 27\"",
  "current_status": "available",
  "is_bookable": true
}
```

---

### `DELETE /api/v1/assets/{id}`

Soft-delete: sets status to `disposed`. Cannot delete if currently allocated.

**Auth:** ✅ Admin

```json
// Response 200
{
  "id": "ast-003...",
  "current_status": "disposed",
  "message": "Asset disposed successfully"
}
```

```json
// Error 409
{
  "detail": "Cannot dispose asset AF-0001: currently allocated to Priya Sharma"
}
```

---

### `GET /api/v1/assets/{id}/history`

Combined allocation + maintenance history for a single asset.

**Auth:** ✅ Any role

```json
// Response 200
{
  "asset_id": "ast-001...",
  "asset_tag": "AF-0001",
  "allocation_history": [
    {
      "id": "al-001...",
      "employee_name": "Priya Sharma",
      "department_name": "Engineering",
      "status": "active",
      "allocated_at": "2026-06-15T10:00:00Z",
      "expected_return_date": "2026-12-15",
      "returned_at": null
    },
    {
      "id": "al-prev-001...",
      "employee_name": "Raj Patel",
      "department_name": "Engineering",
      "status": "returned",
      "allocated_at": "2026-01-10T09:00:00Z",
      "expected_return_date": "2026-06-10",
      "returned_at": "2026-06-12T14:30:00Z"
    }
  ],
  "maintenance_history": [
    {
      "id": "mnt-001...",
      "description": "Screen flickering issue",
      "priority": "high",
      "status": "resolved",
      "raised_by": "Raj Patel",
      "created_at": "2026-05-20T08:00:00Z",
      "resolved_at": "2026-05-25T16:00:00Z"
    }
  ]
}
```

---

### `GET /api/v1/assets/{id}/qrcode`

Generate and return a QR code image for the asset (encodes the asset tag / detail URL).

**Auth:** ✅ Any role

```
// Response 200
Content-Type: image/png
Body: <binary PNG image>
```

---

# 7. Asset Allocations

> Handles allocate, return, transfer request, and overdue detection.
>
> **Transfer workflow** is modeled via allocation status: `Active` → `PendingTransfer` → `Returned` (old) + new `Active` allocation created.

---

### `GET /api/v1/allocations`

List allocations with filters.

**Auth:** ✅ Any role

**Query Params:** `?asset_id=...&employee_id=...&department_id=...&status=active&page=1&page_size=20`

```json
// Response 200
{
  "items": [
    {
      "id": "al-001...",
      "asset_id": "ast-001...",
      "asset_tag": "AF-0001",
      "asset_name": "MacBook Pro 16\"",
      "employee_id": "a1b2c3d4-...",
      "employee_name": "Priya Sharma",
      "department_id": "d5e6f7a8-...",
      "department_name": "Engineering",
      "status": "active",
      "expected_return_date": "2026-12-15",
      "requested_by": "mgr-001...",
      "approved_by": "mgr-001..."
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

### `GET /api/v1/allocations/{id}`

Single allocation detail.

**Auth:** ✅ Any role

```json
// Response 200
{
  "id": "al-001...",
  "asset_id": "ast-001...",
  "asset_tag": "AF-0001",
  "asset_name": "MacBook Pro 16\"",
  "employee_id": "a1b2c3d4-...",
  "employee_name": "Priya Sharma",
  "department_id": "d5e6f7a8-...",
  "status": "active",
  "expected_return_date": "2026-12-15",
  "requested_by": "mgr-001...",
  "approved_by": "mgr-001...",
  "created_at": "2026-06-15T10:00:00Z"
}
```

---

### `POST /api/v1/allocations`

Allocate an asset. **Conflict check:** if already allocated, returns 409 with current holder info and suggests a transfer request.

**Auth:** ✅ Asset Manager, Department Head

```json
// Request
{
  "asset_id": "ast-001...",
  "employee_id": "a1b2c3d4-...",
  "department_id": "d5e6f7a8-...",
  "expected_return_date": "2026-12-15"
}
```

```json
// Response 201 (success)
{
  "id": "al-new-001...",
  "asset_id": "ast-001...",
  "asset_tag": "AF-0001",
  "employee_name": "Priya Sharma",
  "status": "active",
  "expected_return_date": "2026-12-15",
  "message": "Asset allocated successfully"
}
```

```json
// Error 409 (conflict — already allocated)
{
  "detail": "Asset AF-0001 is currently allocated to Raj Patel (Engineering). Use a transfer request instead.",
  "current_holder": {
    "employee_id": "b2c3d4e5-...",
    "employee_name": "Raj Patel",
    "allocation_id": "al-existing..."
  },
  "suggestion": "POST /api/v1/allocations/transfer-request"
}
```

---

### `PATCH /api/v1/allocations/{id}/return`

Mark an allocation as returned. Captures condition check-in notes. Asset status → `available`.

**Auth:** ✅ Asset Manager

```json
// Request
{
  "return_condition": "good",
  "return_notes": "Minor scratches on the lid, otherwise functional"
}
```

```json
// Response 200
{
  "id": "al-001...",
  "asset_tag": "AF-0001",
  "status": "returned",
  "returned_at": "2026-07-12T10:30:00Z",
  "return_condition": "good",
  "return_notes": "Minor scratches on the lid, otherwise functional",
  "asset_status": "available",
  "message": "Asset returned successfully"
}
```

---

### `GET /api/v1/allocations/overdue`

List all allocations past their expected return date.

**Auth:** ✅ Asset Manager, Admin, Department Head

```json
// Response 200
{
  "items": [
    {
      "id": "al-overdue-001...",
      "asset_tag": "AF-0114",
      "asset_name": "Laptop Dell XPS",
      "employee_name": "Raj Patel",
      "department_name": "Engineering",
      "expected_return_date": "2026-07-01",
      "days_overdue": 11
    }
  ],
  "total": 1
}
```

---

### `POST /api/v1/allocations/transfer-request`

Request to transfer an already-allocated asset to a different employee. Creates a new allocation with status `PendingTransfer`.

**Auth:** ✅ Any role

```json
// Request
{
  "asset_id": "ast-001...",
  "to_employee_id": "c3d4e5f6-...",
  "reason": "Raj moved to a different project, Priya needs this laptop"
}
```

```json
// Response 201
{
  "id": "al-transfer-001...",
  "asset_id": "ast-001...",
  "asset_tag": "AF-0001",
  "from_employee": "Raj Patel",
  "to_employee": "Priya Sharma",
  "status": "pending_transfer",
  "reason": "Raj moved to a different project, Priya needs this laptop",
  "message": "Transfer request created. Awaiting approval."
}
```

---

### `PATCH /api/v1/allocations/{id}/approve-transfer`

Approve a pending transfer. Old allocation → `returned`, new allocation → `active`. Asset stays `allocated`.

**Auth:** ✅ Asset Manager, Department Head

```json
// Response 200
{
  "id": "al-transfer-001...",
  "status": "active",
  "asset_tag": "AF-0001",
  "new_holder": "Priya Sharma",
  "previous_holder": "Raj Patel",
  "message": "Transfer approved. Asset re-allocated to Priya Sharma."
}
```

---

### `PATCH /api/v1/allocations/{id}/reject-transfer`

Reject a pending transfer request.

**Auth:** ✅ Asset Manager, Department Head

```json
// Request
{
  "rejection_reason": "Asset is needed by current holder for ongoing project"
}
```

```json
// Response 200
{
  "id": "al-transfer-001...",
  "status": "cancelled",
  "message": "Transfer request rejected"
}
```

---

# 8. Resource Bookings

> Time-slot booking for shared/bookable assets. Overlap validation enforced.

---

### `GET /api/v1/bookings`

List bookings with filters.

**Auth:** ✅ Any role

**Query Params:** `?asset_id=...&booked_by=...&status=upcoming&page=1&page_size=20`

```json
// Response 200
{
  "items": [
    {
      "id": "bk-001...",
      "asset_id": "ast-002...",
      "asset_tag": "AF-0002",
      "asset_name": "Conference Room B2 Projector",
      "booked_by": "a1b2c3d4-...",
      "booked_by_name": "Priya Sharma",
      "start_time": "2026-07-14T09:00:00Z",
      "end_time": "2026-07-14T10:00:00Z",
      "status": "upcoming",
      "purpose": "Sprint planning meeting"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

### `GET /api/v1/bookings/{id}`

Single booking detail.

**Auth:** ✅ Any role

```json
// Response 200
{
  "id": "bk-001...",
  "asset_id": "ast-002...",
  "asset_tag": "AF-0002",
  "asset_name": "Conference Room B2 Projector",
  "booked_by": "a1b2c3d4-...",
  "booked_by_name": "Priya Sharma",
  "start_time": "2026-07-14T09:00:00Z",
  "end_time": "2026-07-14T10:00:00Z",
  "status": "upcoming",
  "purpose": "Sprint planning meeting",
  "created_at": "2026-07-12T08:00:00Z"
}
```

---

### `POST /api/v1/bookings`

Create a booking. **Overlap validation:** rejects if the time slot conflicts with an existing booking for the same asset.

**Auth:** ✅ Any role

```json
// Request
{
  "asset_id": "ast-002...",
  "start_time": "2026-07-14T10:00:00Z",
  "end_time": "2026-07-14T11:00:00Z",
  "purpose": "Design review session"
}
```

```json
// Response 201 (success — 10:00-11:00 doesn't overlap with existing 9:00-10:00)
{
  "id": "bk-002...",
  "asset_tag": "AF-0002",
  "start_time": "2026-07-14T10:00:00Z",
  "end_time": "2026-07-14T11:00:00Z",
  "status": "upcoming",
  "message": "Booking confirmed"
}
```

```json
// Error 409 (overlap — trying to book 9:30-10:30 when 9:00-10:00 exists)
{
  "detail": "Time slot overlaps with an existing booking",
  "conflicting_booking": {
    "id": "bk-001...",
    "booked_by_name": "Priya Sharma",
    "start_time": "2026-07-14T09:00:00Z",
    "end_time": "2026-07-14T10:00:00Z"
  }
}
```

---

### `PATCH /api/v1/bookings/{id}`

Reschedule a booking. Re-validates overlaps for the new time slot.

**Auth:** ✅ Booking owner

```json
// Request
{
  "start_time": "2026-07-14T14:00:00Z",
  "end_time": "2026-07-14T15:00:00Z"
}
```

```json
// Response 200
{
  "id": "bk-002...",
  "start_time": "2026-07-14T14:00:00Z",
  "end_time": "2026-07-14T15:00:00Z",
  "status": "upcoming",
  "message": "Booking rescheduled"
}
```

---

### `DELETE /api/v1/bookings/{id}`

Cancel a booking. Frees the time slot immediately.

**Auth:** ✅ Booking owner

```json
// Response 200
{
  "id": "bk-002...",
  "status": "cancelled",
  "message": "Booking cancelled"
}
```

---

### `GET /api/v1/bookings/calendar`

Calendar view of bookings for a specific resource in a given month.

**Auth:** ✅ Any role

**Query Params:** `?asset_id=ast-002...&month=2026-07`

```json
// Response 200
{
  "asset_id": "ast-002...",
  "asset_name": "Conference Room B2 Projector",
  "month": "2026-07",
  "bookings": [
    {
      "id": "bk-001...",
      "date": "2026-07-14",
      "start_time": "09:00",
      "end_time": "10:00",
      "booked_by_name": "Priya Sharma",
      "purpose": "Sprint planning meeting",
      "status": "upcoming"
    },
    {
      "id": "bk-003...",
      "date": "2026-07-14",
      "start_time": "14:00",
      "end_time": "15:00",
      "booked_by_name": "Amit Kumar",
      "purpose": "1:1 review",
      "status": "upcoming"
    }
  ]
}
```

---

### `GET /api/v1/bookings/availability`

Check if a time slot is available for a specific resource.

**Auth:** ✅ Any role

**Query Params:** `?asset_id=ast-002...&start=2026-07-14T10:00:00Z&end=2026-07-14T11:00:00Z`

```json
// Response 200
{
  "asset_id": "ast-002...",
  "start_time": "2026-07-14T10:00:00Z",
  "end_time": "2026-07-14T11:00:00Z",
  "is_available": true,
  "conflicts": []
}
```

```json
// Response 200 (not available)
{
  "asset_id": "ast-002...",
  "start_time": "2026-07-14T09:30:00Z",
  "end_time": "2026-07-14T10:30:00Z",
  "is_available": false,
  "conflicts": [
    {
      "id": "bk-001...",
      "start_time": "2026-07-14T09:00:00Z",
      "end_time": "2026-07-14T10:00:00Z",
      "booked_by_name": "Priya Sharma"
    }
  ]
}
```

---

# 9. Maintenance Requests

> Full workflow: Pending → Approved/Rejected → Assigned → In Progress → Resolved

---

### `GET /api/v1/maintenance`

List maintenance requests with filters.

**Auth:** ✅ Any role

**Query Params:** `?asset_id=...&status=pending&priority=high&raised_by=...&page=1&page_size=20`

```json
// Response 200
{
  "items": [
    {
      "id": "mnt-001...",
      "asset_id": "ast-001...",
      "asset_tag": "AF-0001",
      "asset_name": "MacBook Pro 16\"",
      "raised_by": "a1b2c3d4-...",
      "raised_by_name": "Priya Sharma",
      "description": "Screen flickering when running external display",
      "priority": "high",
      "status": "pending",
      "created_at": "2026-07-12T08:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

### `GET /api/v1/maintenance/{id}`

Single maintenance request detail.

**Auth:** ✅ Any role

```json
// Response 200
{
  "id": "mnt-001...",
  "asset_id": "ast-001...",
  "asset_tag": "AF-0001",
  "asset_name": "MacBook Pro 16\"",
  "raised_by": "a1b2c3d4-...",
  "raised_by_name": "Priya Sharma",
  "description": "Screen flickering when running external display",
  "priority": "high",
  "status": "pending",
  "approved_by": null,
  "technician_id": null,
  "technician_name": null,
  "resolution_notes": null,
  "created_at": "2026-07-12T08:00:00Z",
  "resolved_at": null
}
```

---

### `POST /api/v1/maintenance`

Raise a new maintenance request.

**Auth:** ✅ Any role

```json
// Request
{
  "asset_id": "ast-001...",
  "description": "Screen flickering when running external display",
  "priority": "high"
}
```

```json
// Response 201
{
  "id": "mnt-001...",
  "asset_tag": "AF-0001",
  "status": "pending",
  "priority": "high",
  "message": "Maintenance request created. Awaiting approval."
}
```

---

### `PATCH /api/v1/maintenance/{id}/approve`

Approve a pending request. Asset status → `under_maintenance`.

**Auth:** ✅ Asset Manager

```json
// Response 200
{
  "id": "mnt-001...",
  "status": "approved",
  "asset_tag": "AF-0001",
  "asset_status": "under_maintenance",
  "approved_by": "mgr-001...",
  "message": "Maintenance request approved. Asset marked as Under Maintenance."
}
```

---

### `PATCH /api/v1/maintenance/{id}/reject`

Reject a pending request.

**Auth:** ✅ Asset Manager

```json
// Request
{
  "rejection_reason": "Issue not reproducible. Please provide more details."
}
```

```json
// Response 200
{
  "id": "mnt-001...",
  "status": "rejected",
  "message": "Maintenance request rejected"
}
```

---

### `PATCH /api/v1/maintenance/{id}/assign`

Assign a technician to an approved request.

**Auth:** ✅ Asset Manager

```json
// Request
{
  "technician_id": "tech-001..."
}
```

```json
// Response 200
{
  "id": "mnt-001...",
  "status": "assigned",
  "technician_id": "tech-001...",
  "technician_name": "Vikram Singh",
  "message": "Technician assigned"
}
```

---

### `PATCH /api/v1/maintenance/{id}/start`

Mark maintenance as in progress.

**Auth:** ✅ Assigned technician

```json
// Response 200
{
  "id": "mnt-001...",
  "status": "in_progress",
  "message": "Maintenance work started"
}
```

---

### `PATCH /api/v1/maintenance/{id}/resolve`

Resolve the request. Asset status → `available`.

**Auth:** ✅ Assigned technician

```json
// Request
{
  "resolution_notes": "Replaced display cable. Screen tested and working fine."
}
```

```json
// Response 200
{
  "id": "mnt-001...",
  "status": "resolved",
  "asset_tag": "AF-0001",
  "asset_status": "available",
  "resolution_notes": "Replaced display cable. Screen tested and working fine.",
  "resolved_at": "2026-07-14T16:00:00Z",
  "message": "Maintenance resolved. Asset is now Available."
}
```

---

# 10. Audit Cycles

> Admin creates cycles scoped to a department. Auditors verify assets. Closing locks the cycle.

---

### `GET /api/v1/audits`

List audit cycles.

**Auth:** ✅ Admin, Asset Manager

**Query Params:** `?status=open&scope_department_id=...&page=1&page_size=20`

```json
// Response 200
{
  "items": [
    {
      "id": "aud-001...",
      "name": "Q3 2026 Engineering Audit",
      "scope_department_id": "d5e6f7a8-...",
      "scope_department_name": "Engineering",
      "start_date": "2026-07-01",
      "end_date": "2026-07-15",
      "status": "open",
      "auditor_ids": ["u-aud-001...", "u-aud-002..."],
      "total_items": 45,
      "verified_count": 12,
      "discrepancy_count": 2
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

### `GET /api/v1/audits/{id}`

Single audit cycle detail.

**Auth:** ✅ Admin, Asset Manager

```json
// Response 200
{
  "id": "aud-001...",
  "name": "Q3 2026 Engineering Audit",
  "scope_department_id": "d5e6f7a8-...",
  "scope_department_name": "Engineering",
  "start_date": "2026-07-01",
  "end_date": "2026-07-15",
  "status": "open",
  "auditor_ids": ["u-aud-001...", "u-aud-002..."],
  "auditor_names": ["Sneha Roy", "Vikram Singh"],
  "progress": {
    "total_items": 45,
    "verified": 12,
    "missing": 1,
    "damaged": 1,
    "pending": 31
  }
}
```

---

### `POST /api/v1/audits`

Create a new audit cycle. Automatically populates audit items for all assets in the scoped department.

**Auth:** ✅ Admin

```json
// Request
{
  "name": "Q3 2026 Engineering Audit",
  "scope_department_id": "d5e6f7a8-...",
  "start_date": "2026-07-01",
  "end_date": "2026-07-15",
  "auditor_ids": ["u-aud-001...", "u-aud-002..."]
}
```

```json
// Response 201
{
  "id": "aud-001...",
  "name": "Q3 2026 Engineering Audit",
  "status": "open",
  "total_items": 45,
  "message": "Audit cycle created with 45 assets to verify"
}
```

---

### `PATCH /api/v1/audits/{id}`

Update audit cycle metadata (dates, auditors). Only if status is `open`.

**Auth:** ✅ Admin

```json
// Request
{
  "end_date": "2026-07-20",
  "auditor_ids": ["u-aud-001...", "u-aud-002...", "u-aud-003..."]
}
```

```json
// Response 200
{
  "id": "aud-001...",
  "end_date": "2026-07-20",
  "auditor_ids": ["u-aud-001...", "u-aud-002...", "u-aud-003..."],
  "message": "Audit cycle updated"
}
```

---

### `PATCH /api/v1/audits/{id}/close`

Close the audit cycle. **Locks it permanently.** Assets marked `missing` → status becomes `lost`.

**Auth:** ✅ Admin

```json
// Response 200
{
  "id": "aud-001...",
  "status": "closed",
  "closed_at": "2026-07-15T18:00:00Z",
  "summary": {
    "total_items": 45,
    "verified": 42,
    "missing": 2,
    "damaged": 1
  },
  "assets_marked_lost": ["AF-0023", "AF-0067"],
  "message": "Audit cycle closed. 2 assets marked as Lost."
}
```

---

# 11. Audit Findings

> Individual asset verification results within an audit cycle.

---

### `POST /api/v1/audits/{audit_id}/findings`

Submit a verification result for a specific asset.

**Auth:** ✅ Assigned auditor

```json
// Request
{
  "asset_id": "ast-001...",
  "finding": "verified",
  "notes": "Asset found at assigned location, condition good"
}
```

```json
// Response 201
{
  "id": "af-001...",
  "audit_cycle_id": "aud-001...",
  "asset_id": "ast-001...",
  "asset_tag": "AF-0001",
  "auditor_id": "u-aud-001...",
  "finding": "verified",
  "notes": "Asset found at assigned location, condition good",
  "verified_at": "2026-07-10T14:00:00Z"
}
```

**Valid findings:** `verified`, `missing`, `damaged`

---

### `PATCH /api/v1/audits/{audit_id}/findings/{finding_id}`

Update a previously submitted finding (only if audit is still `open`).

**Auth:** ✅ Assigned auditor

```json
// Request
{
  "finding": "damaged",
  "notes": "Found asset but screen is cracked"
}
```

```json
// Response 200
{
  "id": "af-001...",
  "finding": "damaged",
  "notes": "Found asset but screen is cracked",
  "verified_at": "2026-07-10T15:30:00Z"
}
```

---

### `GET /api/v1/audits/{audit_id}/report`

Auto-generated discrepancy report: all findings that are NOT `verified`.

**Auth:** ✅ Admin, Asset Manager

```json
// Response 200
{
  "audit_id": "aud-001...",
  "audit_name": "Q3 2026 Engineering Audit",
  "status": "open",
  "generated_at": "2026-07-12T10:00:00Z",
  "summary": {
    "total_items": 45,
    "verified": 42,
    "missing": 2,
    "damaged": 1
  },
  "discrepancies": [
    {
      "asset_id": "ast-023...",
      "asset_tag": "AF-0023",
      "asset_name": "HP Printer LaserJet",
      "finding": "missing",
      "auditor_name": "Sneha Roy",
      "notes": "Asset not found at registered location",
      "last_known_holder": "Raj Patel"
    },
    {
      "asset_id": "ast-067...",
      "asset_tag": "AF-0067",
      "asset_name": "Standing Desk",
      "finding": "missing",
      "auditor_name": "Vikram Singh",
      "notes": "Desk removed, no record of relocation",
      "last_known_holder": null
    },
    {
      "asset_id": "ast-001...",
      "asset_tag": "AF-0001",
      "asset_name": "MacBook Pro 16\"",
      "finding": "damaged",
      "auditor_name": "Sneha Roy",
      "notes": "Found asset but screen is cracked",
      "last_known_holder": "Priya Sharma"
    }
  ]
}
```

---

# 12. Activity Logs & Notifications

> Unified table: `activity_logs`. Notifications are activity logs with a `recipient_user_id` and `is_read` flag.

---

### `GET /api/v1/activity-logs`

Full audit trail of all actions. Admin only.

**Auth:** ✅ Admin

**Query Params:** `?actor_user_id=...&entity_type=asset&action=asset_created&start_date=2026-07-01&end_date=2026-07-12&page=1&page_size=20`

```json
// Response 200
{
  "items": [
    {
      "id": "log-001...",
      "actor_user_id": "mgr-001...",
      "actor_name": "Asset Manager",
      "action": "asset_created",
      "entity_type": "asset",
      "entity_id": "ast-003...",
      "description": "Registered asset 'Dell Monitor 27\"' (AF-0003)",
      "created_at": "2026-07-12T09:00:00Z"
    },
    {
      "id": "log-002...",
      "actor_user_id": "mgr-001...",
      "actor_name": "Asset Manager",
      "action": "allocation_created",
      "entity_type": "allocation",
      "entity_id": "al-001...",
      "description": "Allocated AF-0001 to Priya Sharma",
      "created_at": "2026-07-12T09:15:00Z"
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

### `GET /api/v1/activity-logs/{id}`

Single log detail.

**Auth:** ✅ Admin

```json
// Response 200
{
  "id": "log-001...",
  "actor_user_id": "mgr-001...",
  "actor_name": "Asset Manager",
  "action": "asset_created",
  "entity_type": "asset",
  "entity_id": "ast-003...",
  "description": "Registered asset 'Dell Monitor 27\"' (AF-0003)",
  "recipient_user_id": null,
  "is_read": null,
  "created_at": "2026-07-12T09:00:00Z"
}
```

---

### `GET /api/v1/notifications`

Get the current user's notifications (activity logs where `recipient_user_id = current_user`).

**Auth:** ✅ Any role

**Query Params:** `?is_read=false&page=1&page_size=20`

```json
// Response 200
{
  "items": [
    {
      "id": "notif-001...",
      "action": "asset_assigned",
      "description": "You have been assigned asset AF-0001 (MacBook Pro 16\")",
      "entity_type": "allocation",
      "entity_id": "al-001...",
      "is_read": false,
      "created_at": "2026-07-12T09:15:00Z"
    },
    {
      "id": "notif-002...",
      "action": "maintenance_approved",
      "description": "Your maintenance request for AF-0001 has been approved",
      "entity_type": "maintenance",
      "entity_id": "mnt-001...",
      "is_read": false,
      "created_at": "2026-07-12T10:00:00Z"
    },
    {
      "id": "notif-003...",
      "action": "booking_reminder",
      "description": "Reminder: Your booking for Conference Room B2 Projector starts in 30 minutes",
      "entity_type": "booking",
      "entity_id": "bk-001...",
      "is_read": true,
      "created_at": "2026-07-14T08:30:00Z"
    }
  ],
  "total": 3,
  "unread_count": 2,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

---

### `PATCH /api/v1/notifications/{id}/read`

Mark a single notification as read.

**Auth:** ✅ Notification owner

```json
// Response 200
{
  "id": "notif-001...",
  "is_read": true,
  "message": "Notification marked as read"
}
```

---

### `PATCH /api/v1/notifications/read-all`

Mark all of the current user's notifications as read.

**Auth:** ✅ Notification owner

```json
// Response 200
{
  "updated_count": 2,
  "message": "All notifications marked as read"
}
```

---

# 13. Reports

> Aggregated analytics for managers and admins.

---

### `GET /api/v1/reports/utilization`

Asset utilization trends — most-used vs idle assets.

**Auth:** ✅ Asset Manager, Admin

**Query Params:** `?period=last_30_days&category_id=...`

```json
// Response 200
{
  "period": "last_30_days",
  "total_assets": 120,
  "utilized_assets": 78,
  "utilization_rate": 65.0,
  "most_used": [
    { "asset_tag": "AF-0001", "name": "MacBook Pro 16\"", "allocation_days": 30 },
    { "asset_tag": "AF-0002", "name": "Conference Room B2 Projector", "booking_count": 45 }
  ],
  "idle_assets": [
    { "asset_tag": "AF-0099", "name": "Old Scanner", "idle_days": 90 }
  ]
}
```

---

### `GET /api/v1/reports/maintenance`

Maintenance frequency by asset or category.

**Auth:** ✅ Asset Manager, Admin

**Query Params:** `?period=last_90_days&group_by=category`

```json
// Response 200
{
  "period": "last_90_days",
  "total_requests": 34,
  "by_category": [
    { "category": "Electronics", "count": 22, "avg_resolution_days": 3.5 },
    { "category": "Vehicles", "count": 8, "avg_resolution_days": 7.2 },
    { "category": "Furniture", "count": 4, "avg_resolution_days": 2.1 }
  ],
  "by_priority": {
    "critical": 5,
    "high": 12,
    "medium": 10,
    "low": 7
  }
}
```

---

### `GET /api/v1/reports/departments`

Department-wise allocation summary.

**Auth:** ✅ Asset Manager, Admin

```json
// Response 200
{
  "departments": [
    {
      "department_id": "d5e6f7a8-...",
      "department_name": "Engineering",
      "total_allocated": 45,
      "total_employees": 24,
      "assets_per_employee": 1.88,
      "overdue_count": 2
    },
    {
      "department_id": "d9a8b7c6-...",
      "department_name": "Marketing",
      "total_allocated": 18,
      "total_employees": 12,
      "assets_per_employee": 1.5,
      "overdue_count": 0
    }
  ]
}
```

---

### `GET /api/v1/reports/bookings`

Booking heatmap — peak usage windows.

**Auth:** ✅ Asset Manager, Admin

**Query Params:** `?asset_id=...&period=last_30_days`

```json
// Response 200
{
  "period": "last_30_days",
  "peak_hours": [
    { "hour": 9, "booking_count": 42 },
    { "hour": 10, "booking_count": 38 },
    { "hour": 14, "booking_count": 35 }
  ],
  "peak_days": [
    { "day": "Monday", "booking_count": 28 },
    { "day": "Wednesday", "booking_count": 25 }
  ],
  "most_booked_assets": [
    { "asset_tag": "AF-0002", "name": "Conference Room B2 Projector", "booking_count": 45 },
    { "asset_tag": "AF-0010", "name": "Meeting Room A1", "booking_count": 38 }
  ]
}
```

---

### `GET /api/v1/reports/retirement`

Assets nearing retirement or due for replacement.

**Auth:** ✅ Asset Manager, Admin

```json
// Response 200
{
  "nearing_retirement": [
    {
      "asset_tag": "AF-0005",
      "name": "Old Laptop ThinkPad",
      "category": "Electronics",
      "age_months": 58,
      "maintenance_count": 8,
      "current_status": "available",
      "recommendation": "Consider retirement — high maintenance frequency"
    }
  ],
  "already_retired": [
    {
      "asset_tag": "AF-0003",
      "name": "Broken Printer",
      "current_status": "retired",
      "retired_since": "2026-05-01"
    }
  ]
}
```

---

### `GET /api/v1/reports/export`

Export report data as CSV or PDF.

**Auth:** ✅ Asset Manager, Admin

**Query Params:** `?report_type=utilization&format=csv&period=last_30_days`

```
// Response 200
Content-Type: text/csv (or application/pdf)
Content-Disposition: attachment; filename="utilization_report_2026-07.csv"
Body: <file binary>
```

---

# Error Response Format

All error responses follow a consistent structure:

```json
// 400 Bad Request
{
  "detail": "Validation error",
  "errors": [
    { "field": "email", "message": "Invalid email format" },
    { "field": "password", "message": "Password must be at least 8 characters" }
  ]
}

// 401 Unauthorized
{
  "detail": "Invalid or expired token"
}

// 403 Forbidden
{
  "detail": "Insufficient permissions. Required role: admin"
}

// 404 Not Found
{
  "detail": "Asset with id 'ast-999...' not found"
}

// 409 Conflict
{
  "detail": "Asset AF-0001 is currently allocated to Raj Patel"
}
```

---

# Pagination Format

All list endpoints return paginated results:

```json
{
  "items": [ ... ],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "pages": 5
}
```

**Query params:** `?page=1&page_size=20` (defaults: page=1, page_size=20, max page_size=100)

---

# Summary

| Module | Endpoints | Key Table |
|---|---|---|
| Auth | 6 | `users` |
| Dashboard | 1 | (aggregates) |
| Departments | 4 | `departments` |
| Categories | 4 | `asset_categories` |
| Users/Employees | 5 | `users` |
| Assets | 7 | `assets` |
| Allocations | 7 | `asset_allocations` |
| Bookings | 7 | `resource_bookings` |
| Maintenance | 8 | `maintenance_requests` |
| Audit Cycles | 5 | `audit_cycles` |
| Audit Findings | 3 | `audit_findings` |
| Activity/Notifications | 5 | `activity_logs` |
| Reports | 5 | (aggregates) |
| **Total** | **67** | **10 tables** |
