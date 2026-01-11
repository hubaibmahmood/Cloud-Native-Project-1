"""Pytest configuration and shared fixtures for testing."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

from src.database.connection import get_db
from src.main import app


# Test database engine (in-memory SQLite for fast tests)
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Test session factory
test_session_factory = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture
async def db_session() -> AsyncSession:
    """Provide async database session for tests.

    Creates tables before each test and drops them after.
    Uses transaction rollback to isolate tests.

    Yields:
        AsyncSession: Test database session
    """
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create session
    async with test_session_factory() as session:
        yield session

    # Drop tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncClient:
    """Provide async HTTP client for API integration tests.

    Overrides database dependency to use test database.

    Args:
        db_session: Test database session

    Yields:
        AsyncClient: Test HTTP client
    """

    # Override database dependency with test session
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # Create test client (newer httpx API uses transport parameter)
    from httpx import ASGITransport

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    # Clean up
    app.dependency_overrides.clear()
