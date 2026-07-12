import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_signup(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/signup",
        json={"name": "Test User", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Account created successfully"
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["role"] == "employee"

@pytest.mark.asyncio
async def test_login(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"
    
@pytest.mark.asyncio
async def test_me(async_client: AsyncClient):
    # login first
    login_res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    token = login_res.json()["access_token"]
    
    response = await async_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
