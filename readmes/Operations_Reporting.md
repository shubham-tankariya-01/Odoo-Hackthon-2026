# AssetFlow - Operations & Reporting Module

This document outlines the backend architecture and modules implemented for the Operations and Reporting domain of the AssetFlow project.

All backend features for this domain have been completed using FastAPI, SQLAlchemy (Async), and PostgreSQL, strictly adhering to the Controller-Service-Repository architecture.

---

## Modules Implemented

### 1. Resource Bookings (app/routers/bookings.py)
Allows employees to reserve shared assets (like projectors or conference rooms) for specific time slots.
- Models: ResourceBooking
- Features Built:
  - Conflict Validation: Automatically rejects bookings if the requested time slot overlaps with an existing booking for the same asset.
  - Calendar View: Fetches all bookings for a specific asset in a given month.
  - CRUD operations for creating, rescheduling, and cancelling bookings.

### 2. Activity Logs & Notifications (app/routers/activity_logs.py)
A unified auditing and notification system for the entire application.
- Models: ActivityLog
- Features Built:
  - Global Audit Trail: A system-wide log of all actions taken (e.g., asset created, maintenance approved) for Admin visibility.
  - User Notifications: Personalized alerts routed to specific users.
  - Read Receipts: Endpoints to mark single or all notifications as read.
  - Shared Service: Exposes ActivityLogService.log_action() to easily trigger events from other modules.

### 3. Audits (app/routers/audits.py)
Tracks physical asset verification cycles (e.g., Annual IT Inventory Check).
- Models: AuditCycle, AuditFinding
- Features Built:
  - Cycle Management: Create time-bound audit cycles scoped to specific departments and assigned to specific auditors using PostgreSQL ARRAY(UUID).
  - Dynamic Progress: Automatically calculates the number of missing, verified, and damaged items dynamically when fetching a cycle.
  - Validation: Prevents an Audit Cycle from being closed if any findings remain in a "pending" status.

### 4. Dashboard (app/routers/dashboard.py)
Aggregates high-level Key Performance Indicators (KPIs) for the operational overview.
- Features Built:
  - Real-time calculation of active bookings.
  - Data aggregation handling for pending transfers, upcoming returns, and maintenance items.
  
### 5. Reports (app/routers/reports.py)
Generates structured analytical data for administrators.
- Features Built:
  - Endpoints for calculating asset utilization rates, maintenance frequencies, and department-wise allocations.
  - Dynamic CSV Export: A robust export endpoint that dynamically generates and streams a real .csv file directly to the user's browser based on the report type.

---

## Architecture Pattern Used

Every module in this domain follows a strict 4-layer architecture:

1. Router (routers/): Defines the FastAPI endpoints, handles HTTP methods, and injects dependencies (like the current user and DB session).
2. Controller (controllers/): Receives the HTTP request, handles HTTPExceptions (like 404 Not Found), and maps the request to the Service.
3. Service (services/): Contains pure Python business logic (e.g., checking for time-slot overlaps, calculating audit progress).
4. Repository (repositories/): Contains all SQLAlchemy asynchronous database queries (select, insert, update).

---

## How to Run

1. Ensure your PostgreSQL database credentials are correct in backend/.env.
2. Open your terminal in the backend folder and run the database migrations to create the tables:
   ```bash
   alembic revision --autogenerate -m "Add operations and reporting tables"
   alembic upgrade head
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```
4. View the Swagger API Documentation at: http://localhost:8000/docs
