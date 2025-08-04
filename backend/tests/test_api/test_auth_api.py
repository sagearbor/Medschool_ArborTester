import pytest
from faker import Faker
from backend.api.v1.auth import oauth
from backend.models import Identity

fake = Faker()

@pytest.mark.asyncio
async def test_signup_success(async_client):
    email = fake.email()
    password = fake.password()
    response = await async_client.post(
        "/api/v1/auth/signup",
        json={"name": "Test User", "email": email, "password": password},
    )
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully."

@pytest.mark.asyncio
async def test_signup_conflict_on_existing_email(async_client):
    email = fake.email()
    password = fake.password()
    await async_client.post(
        "/api/v1/auth/signup",
        json={"name": "Test User", "email": email, "password": password},
    )
    response = await async_client.post(
        "/api/v1/auth/signup",
        json={"name": "Another User", "email": email, "password": "anotherpassword"},
    )
    assert response.status_code == 409

@pytest.mark.asyncio
async def test_login_success(async_client):
    email = fake.email()
    password = fake.password()
    await async_client.post(
        "/api/v1/auth/signup",
        json={"name": "Test User", "email": email, "password": password},
    )
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_failure_with_wrong_password(async_client):
    email = fake.email()
    password = fake.password()
    await async_client.post(
        "/api/v1/auth/signup",
        json={"name": "Test User", "email": email, "password": password},
    )
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "wrongpassword"},
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_google_callback_creates_user(async_client, db_session, monkeypatch):
    mock_user_info = {
        "sub": "1234567890",
        "name": "Google User",
        "email": "google.user@example.com",
    }
    
    async def mock_authorize_access_token(request):
        return {"userinfo": mock_user_info}

    monkeypatch.setattr(
        oauth.google,
        "authorize_access_token",
        mock_authorize_access_token
    )

    response = await async_client.get("/api/v1/auth/google/callback")

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

    identity = db_session.query(Identity).filter(Identity.provider_user_id == "1234567890").first()
    assert identity is not None
    assert identity.provider == "google"
    assert identity.user.email == "google.user@example.com"

@pytest.mark.asyncio
async def test_sso_login_placeholder(async_client):
    response = await async_client.post(
        "/api/v1/auth/sso/login",
        json={"email": "student@schoolexample.com"},
    )
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_sso_callback_placeholder(async_client):
    response = await async_client.post("/api/v1/auth/sso/callback")
    assert response.status_code == 200
    assert "callback received" in response.json()["message"]