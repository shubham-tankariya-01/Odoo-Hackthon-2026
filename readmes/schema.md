# AssetFlow Database Schema

## Overview

AssetFlow is built around **10 core entities**.

The central entity is **Asset**, with workflows branching into:

- Asset Allocation
- Resource Booking
- Maintenance
- Audits
- Activity Logging

---

# Entity Relationship Overview

```text
                           Departments
                          ┌────────────┐
                          │            │
                          └─────┬──────┘
                                │
                employs         │
                                ▼
                           ┌─────────┐
                           │  Users  │
                           └────┬────┘
                                │
        ┌──────────────┬────────┼──────────┬──────────────┐
        │              │        │          │              │
        ▼              ▼        ▼          ▼              ▼
 Asset Alloc.     Bookings  Maintenance  Activity      Audit
                                          Logs        Findings


                   Asset Categories
                         │
                         ▼
                    ┌────────┐
                    │ Assets │
                    └───┬────┘
                        │
      ┌─────────────────┼──────────────────────┐
      ▼                 ▼                      ▼
Allocations        Bookings             Maintenance
      │
      ▼
Transfer Workflow
(via Allocation Status)

Departments
      │
      ▼
Audit Cycles
      │
      ▼
Audit Findings
```

---

# Tables

---

## USERS

Represents every employee in the organization.

| Column | Type | Description |
|---------|------|-------------|
| id | UUID | Primary Key |
| name | String | Employee name |
| email | String | Unique email |
| role | Enum/String | System role |
| department_id | UUID | Department |
| promoted_by | UUID | User who assigned role |
| status | String | Active / Inactive |

### Relationships

- belongs to Department
- can create Asset Allocations
- can create Resource Bookings
- can raise Maintenance Requests
- can perform Activity Logs

---

## DEPARTMENTS

Organizational hierarchy.

| Column | Type |
|---------|------|
| id | UUID |
| name | String |
| parent_department_id | UUID |
| head_user_id | UUID |
| status | String |

### Relationships

- has many Users
- has many Asset Allocations
- has many Audit Cycles
- self-referencing parent department

---

## ASSET_CATEGORIES

Defines asset types.

Example:

- Laptop
- Vehicle
- Projector
- Printer

| Column | Type |
|---------|------|
| id | UUID |
| name | String |
| field_schema | JSONB |

### Relationships

- has many Assets

---

## ASSETS

Core entity of the system.

| Column | Type |
|---------|------|
| id | UUID |
| asset_tag | String |
| serial_number | String |
| category_id | UUID |
| current_status | String |
| is_bookable | Boolean |
| custom_fields | JSONB |

### Relationships

- belongs to Asset Category
- has many Asset Allocations
- has many Resource Bookings
- has many Maintenance Requests
- has many Audit Findings

---

## ASSET_ALLOCATIONS

Tracks ownership and transfer lifecycle.

| Column | Type |
|---------|------|
| id | UUID |
| asset_id | UUID |
| employee_id | UUID |
| department_id | UUID |
| status | String |
| expected_return_date | Date |
| requested_by | UUID |
| approved_by | UUID |

### Relationships

- belongs to Asset
- belongs to User
- belongs to Department

### Status Examples

- Active
- Returned
- PendingTransfer
- Cancelled

---

## RESOURCE_BOOKINGS

Tracks temporary reservations.

| Column | Type |
|---------|------|
| id | UUID |
| asset_id | UUID |
| booked_by | UUID |
| start_time | Timestamp |
| end_time | Timestamp |
| status | String |

### Relationships

- belongs to Asset
- belongs to User

---

## MAINTENANCE_REQUESTS

Tracks repair lifecycle.

| Column | Type |
|---------|------|
| id | UUID |
| asset_id | UUID |
| raised_by | UUID |
| approved_by | UUID |
| status | String |
| priority | String |

### Relationships

- belongs to Asset
- raised by User
- approved by User

---

## AUDIT_CYCLES

Represents scheduled asset audits.

| Column | Type |
|---------|------|
| id | UUID |
| scope_department_id | UUID |
| start_date | Date |
| end_date | Date |
| status | String |
| auditor_ids | UUID[] |

### Relationships

- scoped to Department
- produces Audit Findings

---

## AUDIT_FINDINGS

Individual verification results.

| Column | Type |
|---------|------|
| id | UUID |
| audit_cycle_id | UUID |
| asset_id | UUID |
| auditor_id | UUID |
| finding | String |

### Relationships

- belongs to Audit Cycle
- belongs to Asset
- verified by User

---

## ACTIVITY_LOGS

Unified audit trail and notification system.

| Column | Type |
|---------|------|
| id | UUID |
| actor_user_id | UUID |
| recipient_user_id | UUID |
| action | String |
| entity_type | String |
| is_read | Boolean |

### Relationships

- performed by User
- optionally delivered to User

---

# Core Workflows

## Asset Lifecycle

```text
Available
    │
    ├────────────► Allocated
    │                  │
    │                  ▼
    │           Pending Transfer
    │                  │
    │                  ▼
    │             Returned
    │                  │
    └──────────────────┘

Available
    │
    ▼
Booked
    │
    ▼
Available

Available
    │
    ▼
Under Maintenance
    │
    ▼
Available
```

---

# Main Relationships

```text
Department
    └── Users

Department
    └── Asset Allocations

Department
    └── Audit Cycles

Asset Category
    └── Assets

Asset
    ├── Asset Allocations
    ├── Resource Bookings
    ├── Maintenance Requests
    └── Audit Findings

Audit Cycle
    └── Audit Findings

User
    ├── Asset Allocations
    ├── Resource Bookings
    ├── Maintenance Requests
    ├── Audit Findings
    └── Activity Logs
```

---

# Design Decisions

To keep the schema lightweight for the hackathon:

- **Roles** are stored as an enum (`users.role`) instead of separate role tables.
- **Dynamic asset attributes** are stored in `assets.custom_fields` (JSONB).
- **Category metadata** is stored in `asset_categories.field_schema`.
- **Transfer requests** are represented through allocation statuses (e.g., `PendingTransfer`).
- **Notifications** are merged into `activity_logs` using `recipient_user_id` and `is_read`.
- **Audit assignees** are stored as a UUID array (`auditor_ids`) in `audit_cycles`.

---

# Total Tables

1. Users
2. Departments
3. Asset Categories
4. Assets
5. Asset Allocations
6. Resource Bookings
7. Maintenance Requests
8. Audit Cycles
9. Audit Findings
10. Activity Logs