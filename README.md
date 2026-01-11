# Task Management API

A production-ready REST API for managing tasks with full CRUD operations, built with FastAPI and following Clean Architecture principles.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ Task filtering by status, priority, and tags
- ✅ Pagination support
- ✅ Optimistic locking for concurrent updates
- ✅ Clean Architecture with layered separation
- ✅ Comprehensive test suite (contract, integration, unit)
- ✅ API versioning (v1)
- ✅ Structured logging
- ✅ PostgreSQL with SQLModel ORM

## Architecture

The project follows **Clean Architecture** with clear separation of concerns:

```
src/
├── api/
│   ├── v1/
│   │   ├── endpoints/      # HTTP routes (handles requests/responses)
│   │   └── router.py       # API v1 router aggregation
│   ├── schemas/            # Request/response Pydantic models
│   └── dependencies.py     # Dependency injection chain
├── services/               # Business logic layer
├── repositories/           # Data access layer (database queries)
├── models/                 # SQLModel entities (database schema)
├── database/               # Database configuration
└── utils/                  # Shared utilities (logging, settings)
```

### Layer Responsibilities

1. **API Layer** (`api/`): Handles HTTP requests/responses, NO business logic
2. **Service Layer** (`services/`): Business rules, validation, orchestration
3. **Repository Layer** (`repositories/`): Database queries, CRUD operations

### Dependency Injection Chain

```
Database Session → Repository → Service → Route
```

## Prerequisites

- Python 3.12+
- UV package manager
- PostgreSQL (Neon serverless recommended)

## Setup

### 1. Clone and Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd task-management

# Install dependencies with UV
uv sync
```

### 2. Configure Environment

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and set your database URL:

```
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
LOG_LEVEL=INFO
```

### 3. Run Database Migrations

```bash
# Initialize Alembic (if not done)
uv run alembic init migrations

# Create migration
uv run alembic revision --autogenerate -m "Create task table"

# Apply migration
uv run alembic upgrade head
```

### 4. Run the API Server

```bash
uv run uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

All endpoints are prefixed with `/api/v1`:

#### Create Task
```http
POST /api/v1/tasks/
Content-Type: application/json

{
  "title": "Complete project report",
  "description": "Finalize Q4 report",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-01-15T18:00:00Z",
  "tags": ["urgent", "documentation"],
  "estimated_hours": 8.5
}
```

#### Get Task by ID
```http
GET /api/v1/tasks/{task_id}
```

#### List All Tasks (with filtering)
```http
GET /api/v1/tasks/?status=pending&priority=high&tag=urgent&limit=50&offset=0
```

#### Update Task (Partial)
```http
PATCH /api/v1/tasks/{task_id}?If-Match=1
Content-Type: application/json

{
  "status": "completed",
  "title": "Updated title"
}
```

#### Delete Task
```http
DELETE /api/v1/tasks/{task_id}
```

## Running Tests

The project includes comprehensive tests organized in three layers:

- **Contract tests**: Data model validation
- **Integration tests**: End-to-end API workflows
- **Unit tests**: Business logic

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest --cov=src --cov-report=html --cov-report=term

# Run specific test types
uv run pytest tests/contract/ -v      # Contract tests only
uv run pytest tests/integration/ -v   # Integration tests only
uv run pytest tests/unit/ -v          # Unit tests only
```

## Code Quality

```bash
# Format code
uv run black src/ tests/

# Lint code
uv run ruff check src/ tests/ --fix

# Type checking
uv run mypy src/
```

## Project Structure

```
task-management/
├── src/                       # Application source code
│   ├── api/                  # API layer
│   │   ├── v1/              # API version 1
│   │   │   ├── endpoints/   # Route handlers
│   │   │   └── router.py    # Router aggregation
│   │   ├── schemas/         # Pydantic schemas
│   │   └── dependencies.py  # Dependency injection
│   ├── services/            # Business logic
│   ├── repositories/        # Data access
│   ├── models/              # Database models
│   ├── database/            # DB configuration
│   ├── utils/               # Utilities
│   └── main.py              # FastAPI app
│
├── tests/                   # Test suite
│   ├── contract/           # Model tests
│   ├── integration/        # API tests
│   ├── unit/               # Business logic tests
│   └── conftest.py         # Test fixtures
│
├── specs/                  # Feature specifications
├── migrations/             # Database migrations
├── .env                    # Environment variables (not in git)
├── .env.example            # Example environment file
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## Development Workflow

### Adding a New Endpoint

1. **Create/Update Model** (`src/models/`)
2. **Create Repository Methods** (`src/repositories/`)
3. **Create Service Methods** (`src/services/`)
4. **Create API Schemas** (`src/api/schemas/`)
5. **Create Route Handler** (`src/api/v1/endpoints/`)
6. **Write Tests** (`tests/`)

### Testing Strategy

Follow **TDD (Test-Driven Development)**:

1. **RED**: Write failing tests first
2. **GREEN**: Write minimal code to pass tests
3. **REFACTOR**: Improve code while keeping tests green

## Health Check

```bash
# Check if API is running
curl http://localhost:8000/health

# Response:
{
  "status": "healthy"
}
```

## Technology Stack

- **Framework**: FastAPI 0.115+
- **ORM**: SQLModel 0.0.22+
- **Database**: PostgreSQL (via asyncpg)
- **Validation**: Pydantic v2
- **Testing**: pytest, pytest-asyncio, httpx
- **Package Manager**: UV
- **Python**: 3.12+

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes
4. Ensure all tests pass (`uv run pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

MIT License

## Contact

For questions or support, please open an issue on GitHub.
