# Technology Research: Task Management API

**Feature**: 001-task-api
**Date**: 2026-01-08
**Status**: Phase 0 Complete

## Purpose

This document consolidates research findings for technology choices and implementation patterns required for the Task Management API. Each decision is documented with rationale and alternatives considered to support architectural decision-making.

---

## 1. Web Framework Selection

### Decision: FastAPI

**Rationale**:
- **High Performance**: Built on Starlette/ASGI with async support, achieving 20k+ req/s in benchmarks
- **Automatic API Documentation**: OpenAPI/Swagger UI generation aligns with FR-016 (clear API documentation)
- **Pydantic Integration**: Native validation using Pydantic v2 reduces boilerplate and ensures type safety
- **Modern Python**: Leverages Python 3.7+ features (type hints, async/await)
- **Developer Experience**: Excellent IDE support, intuitive decorator-based routing
- **Production Ready**: Used by Microsoft, Uber, Netflix with proven scalability

**Alternatives Considered**:
1. **Flask**: Simpler but requires manual validation, lacks native async, no auto-documentation
2. **Django REST Framework**: More opinionated, heavier ORM (Django ORM), longer startup time, less suitable for lightweight APIs
3. **Starlette**: Lower-level framework requiring more boilerplate for common API patterns

**Best Practices**:
- Use APIRouter for modular endpoint organization
- Implement dependency injection for database sessions
- Enable CORS middleware for cross-origin access if needed
- Use Pydantic models for request/response validation
- Implement exception handlers for consistent error responses

---

## 2. ORM and Data Validation

### Decision: SQLModel

**Rationale**:
- **Unified Models**: Combines SQLAlchemy (ORM) and Pydantic (validation) into single model definitions
- **Type Safety**: Full type hint support with mypy compatibility
- **FastAPI Integration**: Seamless integration with FastAPI's validation layer
- **Async Support**: Works with asyncpg for high-performance async database operations
- **Maintainer**: Created by FastAPI author (Sebastián Ramírez), ensuring ecosystem alignment
- **Reduced Boilerplate**: Eliminates need for separate ORM models and API schemas in many cases

**Alternatives Considered**:
1. **SQLAlchemy + Pydantic**: More mature but requires duplicate model definitions (ORM vs schema)
2. **Tortoise ORM**: Pure async but less mature ecosystem, lacks Pydantic integration
3. **Prisma**: Great DX but requires Node.js toolchain, adds complexity to Python-only stack

**Best Practices**:
- Define table=True models for database entities
- Use separate Pydantic models for API request/response when needed (to control what's exposed)
- Leverage Field() for validation constraints (max_length, regex patterns)
- Use relationships sparingly (keep data model simple per YAGNI)
- Enable SQLModel's async session support

**Version Tracking Pattern**:
```python
from sqlmodel import Field, SQLModel
from datetime import datetime, UTC

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    status: str = Field(default="pending")
    version: int = Field(default=1)  # Optimistic locking
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
```

---

## 3. Database Selection

### Decision: Neon Serverless PostgreSQL

**Rationale**:
- **PostgreSQL Compatibility**: Full ACID compliance, robust transaction support
- **Serverless Architecture**: Auto-scaling, pay-per-use pricing, instant provisioning
- **Connection Pooling**: Built-in connection management reduces overhead
- **Developer Experience**: Easy setup, generous free tier, no infrastructure management
- **Modern Features**: Supports branching (database per feature branch), instant restores
- **Python Support**: Works seamlessly with asyncpg driver

**Alternatives Considered**:
1. **Self-hosted PostgreSQL**: Requires infrastructure management, less cost-effective for MVP
2. **SQLite**: No concurrent write support, insufficient for production use cases
3. **MySQL**: Less feature-rich than PostgreSQL, weaker JSON/array support
4. **Supabase**: Heavier (includes auth, storage, realtime), more than needed

**Best Practices**:
- Use connection pooling (Neon provides this by default)
- Store DATABASE_URL in .env file (never commit credentials)
- Use migrations for schema changes (Alembic integration)
- Enable SSL connections in production
- Monitor connection limits and query performance

**Connection Pattern**:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

---

## 4. Testing Framework and Strategy

### Decision: pytest with pytest-asyncio

**Rationale**:
- **Industry Standard**: Most popular Python testing framework with rich plugin ecosystem
- **Async Support**: pytest-asyncio enables testing of async FastAPI endpoints
- **Fixture System**: Powerful dependency injection for test setup/teardown
- **Parametrization**: Easy to test multiple scenarios with @pytest.mark.parametrize
- **Coverage Integration**: Works seamlessly with pytest-cov for coverage reporting
- **httpx Integration**: httpx.AsyncClient for testing FastAPI apps without running server

**Alternatives Considered**:
1. **unittest**: Built-in but more verbose, less intuitive fixture management
2. **nose2**: Less actively maintained, smaller ecosystem
3. **pytest-bdd**: Adds BDD layer (Given/When/Then), but spec already provides acceptance scenarios

**Testing Layers**:

1. **Contract Tests** (tests/contract/):
   - Verify data model behavior (validation, defaults, versioning)
   - Test SQLModel CRUD operations at ORM level
   - Example: Task creation with missing title should raise validation error

2. **Integration Tests** (tests/integration/):
   - End-to-end API workflows via HTTP
   - Test full user scenarios from spec.md
   - Example: POST /tasks → GET /tasks/{id} → PATCH /tasks/{id} → DELETE /tasks/{id}

3. **Unit Tests** (tests/unit/):
   - Business logic in services layer
   - Validation functions
   - Example: Optimistic locking conflict detection logic

**Best Practices**:
- Use async fixtures for database sessions
- Use httpx.AsyncClient for API integration tests
- Isolate test database (use transactions with rollback)
- Mock external dependencies (if any are added)
- Run tests in parallel with pytest-xdist for speed
- Achieve >90% code coverage

**Test Configuration (conftest.py)**:
```python
import pytest
from httpx import AsyncClient
from sqlmodel import create_engine
from sqlmodel.pool import StaticPool

@pytest.fixture
async def client():
    # In-memory SQLite for fast tests
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Create tables, initialize app
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
```

---

## 5. Optimistic Locking Implementation

### Decision: Version Field with 409/412 Conflict Response

**Rationale**:
- **Data Integrity**: Prevents lost updates when multiple clients modify same task
- **Simple Implementation**: Single integer version field, increment on update
- **RESTful**: HTTP 409 Conflict or 412 Precondition Failed aligns with REST semantics
- **Explicit**: Forces client to handle conflicts (retry with fresh data)
- **Scalable**: No locking overhead, works across distributed systems

**Alternatives Considered**:
1. **Pessimistic Locking**: SELECT FOR UPDATE - blocks concurrent access, reduces throughput
2. **Last-Write-Wins**: Simpler but risks silent data loss (violates FR-014)
3. **Timestamps**: Less reliable (clock skew, precision issues)

**Implementation Pattern**:
```python
async def update_task(task_id: int, updates: TaskUpdate, current_version: int):
    # Read current state
    task = await session.get(Task, task_id)
    if task.version != current_version:
        raise HTTPException(status_code=409, detail="Version conflict")

    # Apply updates
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(task, key, value)

    # Increment version
    task.version += 1
    task.updated_at = datetime.now(UTC)

    await session.commit()
    return task
```

**API Contract**:
- Client sends current version in request (query param or If-Match header)
- Server returns 409 Conflict if version mismatch
- Response includes current version for client to retry

---

## 6. Structured Logging

### Decision: Python standard logging with JSON formatter

**Rationale**:
- **Standard Library**: No additional dependencies, works with all Python tools
- **Structured Output**: JSON format enables log aggregation and analysis
- **Context Enrichment**: Include request_id, user context, duration in logs
- **Performance**: Minimal overhead compared to print statements
- **Integration**: Works with CloudWatch, Datadog, ELK stack, etc.

**Alternatives Considered**:
1. **structlog**: More features but adds dependency, overkill for basic needs
2. **loguru**: Beautiful console output but heavier, less standard
3. **Print statements**: Not production-ready, no log levels or filtering

**Best Practices**:
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Include correlation IDs for request tracing
- Log HTTP requests (method, path, status, duration)
- Log errors with stack traces
- Avoid logging sensitive data (passwords, tokens)

**Configuration Pattern**:
```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# Configure logger
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("task_api")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

---

## 7. Python Async/Await Patterns

### Decision: Async-first architecture with asyncpg

**Rationale**:
- **Performance**: 3-5x faster than sync psycopg2 for I/O-bound operations
- **Concurrency**: Handle 100+ concurrent requests efficiently (SC-003)
- **FastAPI Native**: FastAPI is built on async foundations (ASGI)
- **Resource Efficiency**: Non-blocking I/O reduces memory per request
- **Modern**: Industry standard for Python web services

**Best Practices**:
- Mark all database operations as async
- Use async/await consistently throughout call stack
- Avoid blocking operations (use asyncio.to_thread for CPU-bound tasks)
- Use async context managers for resource cleanup
- Be cautious with async generators (proper cleanup)

**Pattern**:
```python
from sqlmodel.ext.asyncio.session import AsyncSession

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.get("/tasks/{task_id}")
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.exec(select(Task).where(Task.id == task_id))
    task = result.one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

---

## 8. Error Handling and Validation

### Decision: Pydantic validation + FastAPI exception handlers

**Rationale**:
- **Automatic Validation**: Pydantic validates request data before reaching business logic
- **Clear Errors**: Returns 422 with detailed field-level errors
- **Type Safety**: Leverages Python type hints for runtime validation
- **Consistent Responses**: Custom exception handlers ensure uniform error format
- **FR-009/FR-010 Compliance**: Appropriate error codes and messages for all failure scenarios

**Error Response Format**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Task title is required",
    "details": [
      {
        "field": "title",
        "issue": "Field required"
      }
    ]
  }
}
```

**Best Practices**:
- Use Field() validators for constraints (max_length, regex)
- Create custom exception classes for business logic errors
- Implement global exception handlers for consistent responses
- Return specific error codes (400 for validation, 404 for not found, 409 for conflicts)
- Include helpful error messages (what went wrong + how to fix)

---

## 9. Development Environment

### Decision: UV package manager with Python 3.12+

**Rationale**:
- **Speed**: 10-100x faster than pip for dependency resolution
- **Deterministic**: Lock files ensure reproducible environments
- **Modern**: Built in Rust, actively maintained
- **Simple**: Single command to initialize, sync, run
- **Constitution Mandate**: Required by principle VI

**Best Practices**:
- Initialize with `uv init --package .`
- Separate dev dependencies (pytest, ruff, mypy)
- Pin Python version (3.12+)
- Use `uv run` for all commands (ensures correct environment)
- Commit pyproject.toml and uv.lock to version control

**Project Initialization**:
```bash
uv init --package .
uv add fastapi sqlmodel asyncpg pydantic-settings
uv add --dev pytest pytest-asyncio httpx pytest-cov ruff black mypy
```

---

## 10. API Documentation

### Decision: FastAPI auto-generated OpenAPI + Swagger UI

**Rationale**:
- **Zero Overhead**: Generated automatically from type hints and route definitions
- **Interactive**: Swagger UI allows testing endpoints in browser
- **Standards Compliant**: OpenAPI 3.0 specification
- **Always Current**: Stays in sync with code (no drift)
- **FR-016 Compliance**: Provides clear, consumable API documentation

**Best Practices**:
- Add docstrings to endpoints (appear in docs)
- Use response_model to document response shape
- Document status codes with responses parameter
- Include example values in Pydantic models
- Add tags for endpoint grouping

**Example**:
```python
@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=201,
    tags=["Tasks"],
    summary="Create a new task",
    responses={
        201: {"description": "Task created successfully"},
        400: {"description": "Invalid request data"},
    }
)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new task with title and optional description.

    - **title**: Required, max 200 characters
    - **description**: Optional, max 5000 characters
    - **status**: Defaults to 'pending'
    """
    ...
```

---

## Summary

All technology decisions align with:
- ✅ Constitutional principles (TDD, code quality, modern APIs)
- ✅ Functional requirements (CRUD, validation, concurrency, logging)
- ✅ Success criteria (performance, reliability, testability)
- ✅ YAGNI principle (no unnecessary complexity)

**Next Steps**:
- Phase 1: Generate data-model.md from Task entity specification
- Phase 1: Generate API contracts (OpenAPI schema)
- Phase 1: Create quickstart.md for developers

**Key Architectural Decisions for ADR Consideration**:
1. **FastAPI + SQLModel Stack**: REST framework and unified ORM/validation layer
2. **Neon Serverless PostgreSQL**: Database platform choice
3. **Optimistic Locking via Version Field**: Concurrent access safety strategy

These decisions meet the ADR significance test (impact, alternatives, scope) and should be documented via `/sp.adr` after user review.
