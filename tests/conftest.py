import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session

from app.main import app
from app.config import settings
from app.db.session import get_session_generator

# Test database URL - using in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session():
    """Create a test database session."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session
    
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def client(db_session: Session):
    """Create a test client with database session override."""
    def get_session_override():
        yield db_session
    
    app.dependency_overrides[get_session_generator] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }

@pytest.fixture
def test_admin_data():
    """Sample admin user data for testing."""
    return {
        "username": "admin",
        "email": "admin@example.com", 
        "full_name": "Admin User",
        "password": "adminpassword123"
    } 