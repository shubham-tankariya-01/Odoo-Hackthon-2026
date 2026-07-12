import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_end_to_end_core_flow(async_client: AsyncClient):
    # 1. Auth: Signup and Login
    signup_data = {
        "email": "admin@example.com",
        "password": "password123",
        "name": "Admin User",
        "role": "admin"
    }
    resp = await async_client.post("/api/v1/auth/signup", json=signup_data)
    assert resp.status_code == 201
    assert resp.json()["user"]["role"] == "admin"

    login_data = {
        "email": "admin@example.com",
        "password": "password123"
    }
    resp = await async_client.post("/api/v1/auth/login", json=login_data)
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    user_id = resp.json()["user"]["id"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Departments
    dept_data = {
        "name": "IT Department",
        "status": "active"
    }
    resp = await async_client.post("/api/v1/departments", json=dept_data, headers=headers)
    assert resp.status_code == 201
    dept_id = resp.json()["id"]

    # 3. Categories
    cat_data = {
        "name": "Laptops",
        "description": "Company Laptops",
        "is_active": True
    }
    resp = await async_client.post("/api/v1/categories", json=cat_data, headers=headers)
    assert resp.status_code == 201
    cat_id = resp.json()["id"]

    # 4. Assets
    asset_data = {
        "asset_tag": "LT-001",
        "name": "MacBook Pro",
        "category_id": cat_id,
        "current_status": "available",
        "purchase_date": "2023-01-01",
        "purchase_cost": 2000.0,
        "is_active": True
    }
    resp = await async_client.post("/api/v1/assets", json=asset_data, headers=headers)
    assert resp.status_code == 201
    asset_id = resp.json()["id"]

    # 5. Allocations
    alloc_data = {
        "asset_id": asset_id,
        "employee_id": user_id,  # using the admin user
        "department_id": dept_id,
        "expected_return_date": "2026-12-31"
    }
    resp = await async_client.post("/api/v1/allocations", json=alloc_data, headers=headers)
    assert resp.status_code == 201
    alloc_id = resp.json()["id"]

    # 6. Maintenance
    maint_data = {
        "asset_id": asset_id,
        "description": "Screen flickering",
        "priority": "high"
    }
    resp = await async_client.post("/api/v1/maintenance", json=maint_data, headers=headers)
    assert resp.status_code == 201
    maint_id = resp.json()["id"]

    signup_data_2 = {
        "email": "user2@example.com",
        "password": "password123",
        "name": "User 2"
    }
    resp = await async_client.post("/api/v1/auth/signup", json=signup_data_2)
    user2_id = resp.json()["user"]["id"]

    # 7. Transfers
    trans_data = {
        "asset_id": asset_id,
        "to_employee_id": user2_id,
        "reason": "Need a laptop"
    }
    resp = await async_client.post("/api/v1/transfers", json=trans_data, headers=headers)
    assert resp.status_code == 201

    # 8. Audits
    audit_data = {
        "name": "Q3 IT Audit",
        "scope_department_id": dept_id,
        "start_date": "2026-07-01",
        "end_date": "2026-07-31",
        "auditor_ids": []
    }
    resp = await async_client.post("/api/v1/audits/", json=audit_data, headers=headers)
    assert resp.status_code == 200

    # 9. Bookings
    book_data = {
        "asset_id": asset_id,
        "start_time": "2026-08-01T10:00:00Z",
        "end_time": "2026-08-01T12:00:00Z",
        "purpose": "Meeting"
    }
    resp = await async_client.post("/api/v1/bookings/", json=book_data, headers=headers)
    assert resp.status_code == 200

    # 10. Dashboard
    resp = await async_client.get("/api/v1/dashboard", headers=headers)
    assert resp.status_code == 200

    # 11. Reports
    resp = await async_client.get("/api/v1/reports/utilization", headers=headers)
    assert resp.status_code == 200
    resp = await async_client.get("/api/v1/reports/maintenance", headers=headers)
    assert resp.status_code == 200
    resp = await async_client.get("/api/v1/reports/departments", headers=headers)
    assert resp.status_code == 200
    resp = await async_client.get("/api/v1/reports/bookings", headers=headers)
    assert resp.status_code == 200
    resp = await async_client.get("/api/v1/reports/retirement", headers=headers)
    assert resp.status_code == 200

    # 12. Activity Logs
    resp = await async_client.get("/api/v1/activity", headers=headers)
    assert resp.status_code == 200
