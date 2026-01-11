"""Database connection and session management for async PostgreSQL."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.utils.settings import settings

# Create async engine with connection URL from environment
# In development: disable prepared statement cache to avoid schema change issues
# In production: enable cache for better performance
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    future=True,
    connect_args={
        "prepared_statement_cache_size": 0 if settings.ENVIRONMENT == "development" else 500,
    },
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_tables() -> None:
    """Create all database tables.

    Called on application startup to ensure schema exists.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db() -> AsyncSession:
    """Dependency that provides async database session.

    Yields:
        AsyncSession: Database session for use in endpoints

    Usage:
        @app.get("/tasks")
        async def list_tasks(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session() as session:
        yield session
