import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from httpx import AsyncClient

from backend.main import app
from backend.database import get_db
from backend.models import Base
from backend.auth.jwt import create_access_token

# Test database configuration
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def db_setup():
    """Set up test database"""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session(db_setup):
    """Create a fresh database session for each test"""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def override_get_db(db_session):
    """Override the get_db dependency to use test database"""
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def client(override_get_db):
    """Create test client"""
    return TestClient(app)

@pytest.fixture
async def async_client(override_get_db):
    """Create async test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def async_authenticated_client(override_get_db, auth_headers, db_session):
    """Create authenticated async test client with user"""
    from backend.tests.factories import UserFactory
    UserFactory._meta.sqlalchemy_session = db_session
    
    user = UserFactory(id=1)  # Match the token's sub claim
    async with AsyncClient(app=app, base_url="http://test", headers=auth_headers) as ac:
        yield ac, user

@pytest.fixture
def auth_token():
    """Create a test authentication token"""
    return create_access_token(data={"sub": "1"})

@pytest.fixture
def auth_headers(auth_token):
    """Create authorization headers for testing"""
    return {"Authorization": f"Bearer {auth_token}"}

@pytest.fixture
def authenticated_client(override_get_db, auth_headers, db_session):
    """Create authenticated test client with user"""
    from backend.tests.factories import UserFactory
    UserFactory._meta.sqlalchemy_session = db_session
    
    user = UserFactory(id=1)  # Match the token's sub claim
    client = TestClient(app)
    client.headers.update(auth_headers)
    return client, user