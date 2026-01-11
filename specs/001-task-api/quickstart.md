# Quickstart Guide: Task Management API

**Feature**: 001-task-api
**Target Audience**: Developers setting up the project for the first time
**Estimated Setup Time**: 10-15 minutes

---

## Prerequisites

Before starting, ensure you have:

- **Python 3.12+**: Check with `python3 --version`
- **UV package manager**: Install via `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Neon PostgreSQL account**: Sign up at [neon.tech](https://neon.tech) (free tier available)
- **Git**: For version control

---

## Quick Setup (5 Steps)

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd task-management
git checkout 001-task-api
```

### 2. Initialize Project with UV
```bash
# Create Python package structure
uv init --package .

# Install dependencies (will create virtual environment)
uv add fastapi sqlmodel asyncpg pydantic-settings uvicorn

# Install development dependencies
uv add --dev pytest pytest-asyncio httpx pytest-cov ruff black mypy
```

### 3. Set Up Database
```bash
# Create .env file with your Neon database URL
echo "DATABASE_URL=postgresql+asyncpg://user:password@host/database" > .env

# Example (replace with your actual Neon credentials):
# DATABASE_URL=postgresql+asyncpg://myuser:mypassword@ep-example-123.us-east-2.aws.neon.tech/taskdb
```

**Get your Neon DATABASE_URL**:
1. Go to [Neon Console](https://console.neon.tech)
2. Create a new project (if needed)
3. Copy the connection string from "Connection Details"
4. Replace `postgresql://` with `postgresql+asyncpg://` (required for async driver)

### 4. Run Database Migrations
```bash
# Initialize Alembic (database migration tool)
uv run alembic init migrations

# Generate initial migration
uv run alembic revision --autogenerate -m "Create task table"

# Apply migration
uv run alembic upgrade head
```

### 5. Start the API Server
```bash
# Run development server with auto-reload
uv run uvicorn src.main:app --reload

# Server will start at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

**Verify it's working**:
```bash
curl http://localhost:8000/tasks
# Expected: {"tasks": [], "total": 0, "limit": 50, "offset": 0}
```

---

## Project Structure

After setup, your directory structure should look like:

```
task-management/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py              # Task entity
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py      # CRUD business logic
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── tasks.py         # Task endpoints
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── task.py          # Request/response schemas
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py        # Database session management
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logging.py           # Structured logging
│   └── main.py                  # FastAPI app initialization
│
├── tests/
│   ├── contract/
│   │   └── test_task_model.py
│   ├── integration/
│   │   └── test_task_workflows.py
│   ├── unit/
│   │   └── test_task_service.py
│   └── conftest.py              # Shared pytest fixtures
│
├── .env                         # Environment variables (DATABASE_URL)
├── pyproject.toml               # UV project configuration
└── uv.lock                      # Dependency lock file
```

---

## Development Workflow

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=src --cov-report=html

# Run specific test category
uv run pytest tests/contract/
uv run pytest tests/integration/
uv run pytest tests/unit/

# Run in parallel for speed
uv run pytest -n auto
```

### Code Quality Checks

```bash
# Format code with Black
uv run black src/ tests/

# Lint with Ruff
uv run ruff check src/ tests/

# Type check with mypy
uv run mypy src/

# Run all quality checks at once
uv run black src/ tests/ && uv run ruff check src/ tests/ && uv run mypy src/
```

### TDD Red-Green-Refactor Cycle

1. **Red**: Write a failing test
   ```bash
   # Create test in tests/contract/test_task_model.py
   uv run pytest tests/contract/test_task_model.py::test_create_task
   # Expected: FAILED (test should fail initially)
   ```

2. **Green**: Write minimal code to pass the test
   ```bash
   # Implement feature in src/models/task.py
   uv run pytest tests/contract/test_task_model.py::test_create_task
   # Expected: PASSED
   ```

3. **Refactor**: Improve code quality while keeping tests green
   ```bash
   # Refactor implementation
   uv run pytest  # All tests should still pass
   ```

4. **Commit**: Only commit when all tests pass
   ```bash
   git add .
   git commit -m "feat: Add task creation with validation

   Refs: FR-001, FR-008"
   ```

---

## API Usage Examples

### Interactive API Documentation
Open in browser: [http://localhost:8000/docs](http://localhost:8000/docs)

This provides:
- Interactive endpoint testing
- Request/response schemas
- Example payloads
- Try-it-out functionality

### Creating a Task
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project report",
    "description": "Finalize Q4 report with metrics and analysis",
    "status": "pending",
    "priority": "high",
    "due_date": "2026-01-15T18:00:00Z",
    "tags": ["urgent", "documentation"],
    "estimated_hours": 8.5
  }'
```

**Response** (201 Created):
```json
{
  "id": 1,
  "title": "Complete project report",
  "description": "Finalize Q4 report with metrics and analysis",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-01-15T18:00:00Z",
  "tags": ["urgent", "documentation"],
  "estimated_hours": 8.5,
  "version": 1,
  "created_at": "2026-01-08T10:30:00Z",
  "updated_at": "2026-01-08T10:30:00Z"
}
```

### Listing Tasks
```bash
# Get all tasks
curl http://localhost:8000/tasks

# Filter by status
curl "http://localhost:8000/tasks?status=pending"

# Filter by priority
curl "http://localhost:8000/tasks?priority=high"

# Filter by tag
curl "http://localhost:8000/tasks?tag=urgent"

# Combine filters
curl "http://localhost:8000/tasks?status=pending&priority=high&tag=urgent"

# Paginate results
curl "http://localhost:8000/tasks?limit=10&offset=20"
```

### Retrieving a Task
```bash
curl http://localhost:8000/tasks/1
```

### Updating a Task (with Optimistic Locking)
```bash
# Note the If-Match header with current version
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -H "If-Match: 1" \
  -d '{
    "status": "completed",
    "priority": "medium",
    "tags": ["urgent", "documentation", "done"]
  }'
```

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Complete project report",
  "description": "Finalize Q4 report with metrics and analysis",
  "status": "completed",
  "priority": "medium",
  "due_date": "2026-01-15T18:00:00Z",
  "tags": ["urgent", "documentation", "done"],
  "estimated_hours": 8.5,
  "version": 2,
  "created_at": "2026-01-08T10:30:00Z",
  "updated_at": "2026-01-08T15:45:00Z"
}
```

**Conflict Response** (409 Conflict) - if version mismatch:
```json
{
  "error": {
    "code": "VERSION_CONFLICT",
    "message": "Task was modified by another request. Current version is 3.",
    "current_version": 3,
    "requested_version": 1
  }
}
```

### Deleting a Task
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

**Response**: 204 No Content (success, no body)

---

## Common Issues and Solutions

### Issue: Database Connection Fails
**Symptom**: `asyncpg.exceptions.InvalidCatalogNameError`

**Solution**:
1. Verify DATABASE_URL in `.env` is correct
2. Ensure you're using `postgresql+asyncpg://` prefix (not just `postgresql://`)
3. Check that Neon database is active (may pause on free tier)
4. Test connection: `psql <DATABASE_URL>`

### Issue: Import Errors
**Symptom**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Ensure you're using uv run (activates virtual environment)
uv run python src/main.py

# Or manually activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Issue: Tests Fail with Database Errors
**Symptom**: Tests try to connect to production database

**Solution**:
Update `tests/conftest.py` to use in-memory SQLite for tests:
```python
import pytest
from sqlmodel import create_engine
from sqlmodel.pool import StaticPool

@pytest.fixture
def test_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Create tables
    SQLModel.metadata.create_all(engine)
    return engine
```

### Issue: Port Already in Use
**Symptom**: `OSError: [Errno 48] Address already in use`

**Solution**:
```bash
# Use a different port
uv run uvicorn src.main:app --reload --port 8001

# Or kill the process using port 8000
lsof -ti:8000 | xargs kill -9  # Mac/Linux
```

---

## Next Steps

After completing this quickstart:

1. **Read the Full Specification**: See `specs/001-task-api/spec.md` for all requirements and user scenarios

2. **Review Architecture Design**: See `specs/001-task-api/plan.md` for technical decisions and structure

3. **Explore Data Model**: See `specs/001-task-api/data-model.md` for entity details and validation rules

4. **Check API Contracts**: See `specs/001-task-api/contracts/openapi.yaml` for complete API specification

5. **Start Implementing**: Follow the tasks in `specs/001-task-api/tasks.md` (generated by `/sp.tasks` command)

6. **Follow TDD**: Write failing tests first, then implement features

---

## Useful Commands Cheat Sheet

```bash
# Development
uv run uvicorn src.main:app --reload           # Start dev server
uv run pytest                                  # Run all tests
uv run pytest --cov=src                       # Tests with coverage

# Code Quality
uv run black src/ tests/                       # Format code
uv run ruff check src/ tests/                  # Lint code
uv run mypy src/                               # Type check

# Database
uv run alembic revision --autogenerate -m "msg"  # Create migration
uv run alembic upgrade head                      # Apply migrations
uv run alembic downgrade -1                      # Rollback one migration

# Dependencies
uv add <package>                               # Add production dependency
uv add --dev <package>                         # Add dev dependency
uv sync                                        # Sync dependencies from lock file
```

---

## Getting Help

- **API Documentation**: http://localhost:8000/docs (when server is running)
- **Project Constitution**: `.specify/memory/constitution.md` (coding standards and principles)
- **Feature Specification**: `specs/001-task-api/spec.md`
- **OpenAPI Contract**: `specs/001-task-api/contracts/openapi.yaml`

---

**Happy Coding!** 🚀
