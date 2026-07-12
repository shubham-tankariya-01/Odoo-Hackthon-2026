# AssetFlow Backend Architecture & Phase 1 Summary

This document explains the architecture of the AssetFlow backend and summarizes the foundational work completed in Phase 1. It serves as a guide for all team members jumping into the codebase.

---

## 🏗️ The Layered Architecture (MVC-Style)

To ensure the codebase is maintainable, scalable, and responsibilities are cleanly separated, we enforce a strict data flow for every API request:

**`Router ➔ Controller ➔ Service ➔ Repository ➔ Database`**

### 1. Routers (`app/routers/`)
These files define the API endpoints (e.g., `POST /api/v1/auth/login`). 
*   **Role:** Handle HTTP routing, parameter validation (via Pydantic), and Dependency Injection (like requiring an active user token).
*   **Rule:** Routers contain **no business logic**. They simply route the validated request to a controller.

### 2. Controllers (`app/controllers/`)
These act as the bridge between the web layer (routers) and the business layer (services).
*   **Role:** Receive data from the router, instantiate the required Services/Repositories, call the service methods, and then format the returned data (e.g., converting ORM models to Pydantic JSON structures) to send back to the user.

### 3. Services (`app/services/`)
**This is where all the business logic lives.**
*   **Role:** Enforce business rules. For example, if an admin wants to promote a user, the rules dictating *who* can promote and *when* it's allowed are enforced here. 
*   **Rule:** Services never write raw SQL or touch HTTP request objects directly. They orchestrate rules and call Repositories.

### 4. Repositories (`app/repositories/`)
These files encapsulate all database interactions.
*   **Role:** Handle raw data fetching and saving. For example, `UserRepository.get_by_email()` runs a specific `SELECT` query via SQLAlchemy. 
*   **Note:** The `BaseRepository` provides generic CRUD functions (create, update, delete, get_all, get_by_id) so we don't have to rewrite standard database operations for every model.

### 5. Database (`app/database.py` & PostgreSQL)
*   **Role:** We use **SQLAlchemy 2.0** with `asyncpg` to allow non-blocking, highly concurrent database operations. 

---

## 🛠️ Key Utilities & Patterns

*   **Pydantic Schemas (`app/schemas/`)**: Used for data validation. For every resource, we generally have a `Create` schema (what the client sends), an `Update` schema (with optional fields), and a `Response` schema (what we return, stripping sensitive data like passwords).
*   **SQLAlchemy Models (`app/models/`)**: Define the PostgreSQL database tables. Every model inherits from an abstract `BaseModel` that automatically provides a UUID `id`, `created_at`, and `updated_at`.
*   **Authentication (`app/dependencies/auth.py`)**: Uses JWT (JSON Web Tokens) for stateless authentication. Endpoint dependencies automatically decode incoming tokens, verify the user's status, and enforce Role-Based Access Control (RBAC) (e.g., ensuring a user is an `admin`).
*   **Alembic (`alembic/`)**: Our database migration tool. It reads our SQLAlchemy models and generates the necessary SQL to incrementally update the database schema without manual SQL scripts.

---

## ✅ Summary of Phase 1 Work Completed

Phase 1 focused on building the **Foundation** and **Organization** modules required before the rest of the application (Assets, Bookings, etc.) can be built. 

**Work completed by Member 1:**

1. **Project Scaffolding**
   - Configured the FastAPI app structure and `.env` environment loading.
   - Set up async PostgreSQL connection using SQLAlchemy 2.0.
   - Configured Alembic for async database migrations.
   - Set up `pytest` with an in-memory SQLite database (`aiosqlite`) for testing.

2. **Auth Module**
   - Built full JWT authentication flow (Signup, Login, Password Reset token generation).
   - Created the `get_current_user` dependency for secure session validation.
   - Created `require_role` dependency to protect specific endpoints.
   - Wrote `scripts/seed_admin.py` to programmatically generate the first system Admin.

3. **Departments Module**
   - Implemented CRUD operations for Departments.
   - Added support for hierarchical departments using `parent_department_id`.
   - Added `head_user_id` to assign managers.
   - Enforced rules (e.g., preventing deactivation if active users belong to the department).

4. **Users Module**
   - Added endpoints to list users with filtering (by department, role, or status).
   - Created user profile update endpoints.
   - Created a specific `/promote` endpoint restricted to Admins for changing user roles.

5. **Categories Module**
   - Built foundational CRUD module for `AssetCategory`.
   - Prepares the system for linking Assets to Categories.

### 🚀 Next Steps (For Members 2 & 3)
The framework is fully set up. 
*   **Member 2 (Assets & Allocations)** can now create `app/models/asset.py` which can safely foreign-key into `Category`, `User`, and `Department`.
*   **Member 3 (Operations)** can begin utilizing the robust authentication and department architecture for Bookings and Dashboard endpoints.
