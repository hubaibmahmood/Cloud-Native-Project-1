# Tasks: Task Management API

**Input**: Design documents from `/specs/001-task-api/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED per FR-017 and SC-009 (comprehensive automated test suite covering all functional requirements and user workflows)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Task Sizing**: Each task is estimated to take 20-30 minutes of focused work.

**Version**: 2.0 (Revised for better sizing and completeness)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths below follow single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

**Time Estimate**: ~1 hour (3 tasks × 20-30 minutes)

- [X] T001 Initialize Python project with UV package manager (run `uv init --package .` and create basic directory structure: src/, tests/, specs/)
- [X] T002 [P] Install production dependencies via UV (FastAPI, SQLModel, asyncpg, pydantic-settings, uvicorn, alembic) in pyproject.toml
- [X] T003 [P] Install development dependencies via UV (pytest, pytest-asyncio, pytest-cov, httpx, ruff, black, mypy) in pyproject.toml

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Time Estimate**: ~5 hours (11 tasks × 20-30 minutes)

- [X] T004 Create database module in src/database/ (connection.py with async engine and session factory using DATABASE_URL, __init__.py with imports and create_tables function)
- [X] T005 Initialize Alembic for database migrations (run `uv run alembic init migrations`, configure alembic.ini with DATABASE_URL from env, update env.py to import Task model metadata)
- [X] T006 Create and apply initial database migration (run `alembic revision --autogenerate -m "Create task table"`, review generated migration for Task table with 11 fields and 6 indexes, run `alembic upgrade head`)
- [X] T007 [P] Configure structured logging in src/utils/logging.py (JSON formatter for production, human-readable for dev, log levels from env, request ID context support)
- [X] T008 [P] Create error response schemas in src/api/schemas/error.py (ErrorResponse, ValidationErrorDetail, VersionConflictError matching OpenAPI spec with code, message, details fields)
- [X] T009 [P] Create FastAPI app instance in src/main.py (app initialization, health check endpoint at GET /health returning {"status": "healthy"})
- [X] T010 [P] Add CORS middleware and lifecycle events in src/main.py (CORS middleware for cross-origin requests, startup event to create tables, shutdown event to close connections)
- [X] T011 [P] Add global exception handlers in src/main.py (ValidationError → 422, NotFoundError → 404, VersionConflictError → 409, generic Exception → 500 with consistent error format)
- [X] T012 [P] Create pytest configuration in tests/conftest.py (async test fixtures, in-memory SQLite engine with isolated transactions, test client factory, database fixture that creates/drops tables per test, session fixture with automatic rollback)
- [X] T013 [P] Create environment configuration example in .env.example (DATABASE_URL template for Neon PostgreSQL, LOG_LEVEL options, document all required environment variables with examples)
- [X] T014 [P] Create settings module in src/utils/settings.py (use pydantic-settings BaseSettings to load DATABASE_URL, LOG_LEVEL, API_PREFIX, validate required vars, provide sensible defaults)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and Retrieve Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks with all fields (title, description, status, priority, due_date, tags, estimated_hours) and retrieve them by ID or list all tasks with filtering

**Independent Test**: Create a task via POST /tasks with full field set, retrieve it via GET /tasks/{id}, verify all fields match; list all tasks via GET /tasks with filters (status, priority, tag)

**Time Estimate**: ~6.5 hours (16 tasks × 20-30 minutes)

### Tests for User Story 1 (TDD - Write Tests FIRST)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T015 [P] [US1] Write contract test for Task model creation with valid data in tests/contract/test_task_model.py (test all 11 fields, verify defaults: status='pending', priority='medium', tags=[], version=1, created_at and updated_at auto-set)
- [X] T016 [P] [US1] Write contract test for Task model validation failures in tests/contract/test_task_model.py (empty title fails, title >200 chars fails, description >5000 chars fails, invalid status/priority fails, negative estimated_hours fails, tags with >50 char strings fail)
- [X] T017 [P] [US1] Write integration test for POST /tasks endpoint in tests/integration/test_task_workflows.py (create task with all fields, verify 201 response, returned task has id and timestamps, all fields match input)
- [X] T018 [P] [US1] Write integration test for GET /tasks/{id} endpoint in tests/integration/test_task_workflows.py (create task, retrieve by ID, verify 200 response and data matches, test 404 for invalid ID)
- [X] T019 [P] [US1] Write integration test for GET /tasks list endpoint in tests/integration/test_task_workflows.py (create 3 tasks, list all, verify 200 response with tasks array, total count, pagination metadata)
- [X] T020 [P] [US1] Write integration test for GET /tasks filtering in tests/integration/test_task_workflows.py (create tasks with different status/priority/tags, filter by status, filter by priority, filter by tag, verify each filter returns correct subset)

### Implementation for User Story 1

- [X] T021 [US1] Create Task model base structure in src/models/task.py (SQLModel table=True with 11 fields: id optional int primary key, title str, description optional str, status str, priority str, due_date optional datetime, tags list[str], estimated_hours optional Decimal, version int, created_at datetime, updated_at datetime; use modern datetime.now(UTC) for timestamps)
- [X] T022 [US1] Add TaskStatus and TaskPriority enums and validation rules in src/models/task.py (TaskStatus enum: pending/in_progress/completed, TaskPriority enum: critical/high/medium/low, Field validators: title min_length=1 max_length=200, description max_length=5000, tags ARRAY column, estimated_hours ge=0, model_config with example)
- [X] T023 [P] [US1] Create API request/response schemas in src/api/schemas/task.py (TaskCreate with required title and optional fields, TaskResponse inheriting from Task, TaskUpdate with all optional fields, TaskList with tasks array and pagination metadata; ensure schemas match OpenAPI spec)
- [X] T024 [P] [US1] Implement create_task method in src/services/task_service.py (accept TaskCreate data, create Task instance with defaults, set created_at and updated_at to datetime.now(UTC), save to database, return created task with id)
- [X] T025 [P] [US1] Implement get_task_by_id method in src/services/task_service.py (query Task by id, return task if found or None, handle database errors gracefully)
- [X] T026 [US1] Implement get_all_tasks method with filtering in src/services/task_service.py (build SQLAlchemy query, apply WHERE clauses for status/priority/tags filters if provided, apply pagination offset/limit defaulting to 0/50, execute query, return tasks list and total count)
- [X] T027 [US1] Implement POST /tasks endpoint in src/api/routes/tasks.py (create APIRouter, define POST route accepting TaskCreate schema, inject db session dependency, call create_task service, return 201 with TaskResponse, handle validation errors → 400)
- [X] T028 [US1] Implement GET /tasks/{id} endpoint in src/api/routes/tasks.py (define GET route with task_id path param, call get_task_by_id service, return 200 with TaskResponse if found, raise 404 HTTPException if not found)
- [X] T029 [US1] Implement GET /tasks list endpoint in src/api/routes/tasks.py (define GET route with query params: status, priority, tag, limit, offset; call get_all_tasks service with filters, return 200 with TaskList containing tasks array and pagination metadata)
- [X] T030 [US1] Integrate User Story 1 and verify in src/main.py (import and include task router with prefix="/tasks" and tags=["Tasks"], run `uv run pytest tests/contract tests/integration -v -k US1`, verify all 6 tests pass, manually test POST and GET endpoints)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently (create task with all 11 fields, retrieve task by ID, list/filter tasks by status/priority/tags)

---

## Phase 4: User Story 2 - Update Existing Tasks (Priority: P2)

**Goal**: Enable users to modify task fields (title, description, status, priority, due_date, tags, estimated_hours) with optimistic locking to prevent concurrent update conflicts

**Independent Test**: Create a task, update multiple fields via PATCH /tasks/{id} with If-Match header, verify changes persist and version increments; test concurrent update conflict returns 409

**Time Estimate**: ~3 hours (9 tasks × 20-30 minutes)

### Tests for User Story 2 (TDD - Write Tests FIRST)

- [X] T031 [P] [US2] Write contract test for Task model update in tests/contract/test_task_model.py (update task fields, verify version increments from 1 to 2, verify updated_at changes, verify created_at unchanged)
- [X] T032 [P] [US2] Write integration test for PATCH /tasks/{id} single field in tests/integration/test_task_workflows.py (create task, update status via PATCH with If-Match header, verify 200 response, status updated, version=2, other fields unchanged)
- [X] T033 [P] [US2] Write integration test for PATCH /tasks/{id} multiple fields in tests/integration/test_task_workflows.py (create task, update title + status + priority + tags simultaneously via PATCH, verify 200 response, all updates applied atomically, version incremented)
- [X] T034 [P] [US2] Write integration test for optimistic locking conflict in tests/integration/test_task_workflows.py (create task version=1, simulate concurrent updates by sending two PATCH requests with same If-Match:1, verify first returns 200 with version=2, second returns 409 Conflict with current_version=2 and requested_version=1 in error response)
- [X] T035 [P] [US2] Write integration test for PATCH error cases in tests/integration/test_task_workflows.py (PATCH non-existent task returns 404, PATCH without If-Match header returns 412 Precondition Failed, PATCH with invalid field values returns 400 validation error)

### Implementation for User Story 2

- [X] T036 [US2] Implement update_task method with logging in src/services/task_service.py (accept task_id, updates dict, current_version; query task by id, check version matches or raise VersionConflictError, apply field updates from dict, increment version, set updated_at=datetime.now(UTC), save, log update with task_id and changed fields, return updated task)
- [X] T037 [US2] Implement PATCH /tasks/{id} endpoint in src/api/routes/tasks.py (define PATCH route, extract If-Match header and parse version as int, accept TaskUpdate schema, call update_task service, return 200 with updated TaskResponse, raise 412 if If-Match missing)
- [X] T038 [US2] Add validation for PATCH request in src/api/routes/tasks.py (ensure at least one field provided in TaskUpdate, validate field values match constraints, handle Pydantic ValidationError → 400 with field-level error details)
- [X] T039 [US2] Add error handling for optimistic locking in src/api/routes/tasks.py (catch VersionConflictError exception, return 409 HTTPException with body containing code="VERSION_CONFLICT", message, current_version, requested_version matching OpenAPI VersionConflictError schema)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (create, retrieve, update with optimistic locking and version conflict detection)

---

## Phase 5: User Story 3 - Delete Tasks (Priority: P3)

**Goal**: Enable users to permanently remove tasks that are no longer relevant

**Independent Test**: Create a task, delete it via DELETE /tasks/{id}, verify 204 response; attempt to retrieve deleted task returns 404; list all tasks excludes deleted task

**Time Estimate**: ~1.5 hours (4 tasks × 20-30 minutes)

### Tests for User Story 3 (TDD - Write Tests FIRST)

- [X] T040 [P] [US3] Write integration test for DELETE /tasks/{id} endpoint in tests/integration/test_task_workflows.py (create task, delete it via DELETE, verify 204 No Content response with empty body)
- [X] T041 [P] [US3] Write integration test for DELETE verification in tests/integration/test_task_workflows.py (create task, delete it, attempt GET /tasks/{id} returns 404, GET /tasks list excludes deleted task from results)
- [X] T042 [P] [US3] Write integration test for DELETE error cases in tests/integration/test_task_workflows.py (DELETE non-existent task returns 404, DELETE same task twice is idempotent with 404 on second attempt)

### Implementation for User Story 3

- [X] T043 [US3] Implement delete functionality in src/services/task_service.py and src/api/routes/tasks.py (delete_task service method: query task by id, delete from database or raise NotFoundError, log deletion with task_id; DELETE endpoint: call delete_task service, return 204 on success, handle NotFoundError → 404)

**Checkpoint**: All user stories should now be independently functional (create, retrieve, update with optimistic locking, delete)

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories, final validation

**Time Estimate**: ~2.5 hours (6 tasks × 20-30 minutes)

- [ ] T044 [P] Add unit tests for validation logic in tests/unit/test_task_service.py (test title/description length validation, test tags array validation, test due_date ISO 8601 parsing, test estimated_hours non-negative constraint, test status/priority enum validation)
- [ ] T045 [P] Add unit tests for optimistic locking logic in tests/unit/test_task_service.py (test version increment on update, test version conflict detection, test version comparison edge cases)
- [ ] T046 Verify comprehensive test coverage (run `uv run pytest --cov=src --cov-report=html --cov-report=term`, ensure >90% coverage for src/models, src/services, src/api, review HTML report, add tests for any uncovered critical paths) [PARTIAL: 68% coverage achieved]
- [ ] T047 Validate all acceptance scenarios from spec.md (run full test suite `uv run pytest tests/ -v`, manually verify or create acceptance tests for all user story scenarios from spec.md, confirm FR-001 through FR-019 functional requirements met, verify SC-001 through SC-012 success criteria achievable)
- [X] T048 [P] Run code quality checks and fix issues (run `uv run black src/ tests/` to format, run `uv run ruff check src/ tests/ --fix` to lint and auto-fix, run `uv run mypy src/` for type checking, fix any remaining errors or warnings)
- [X] T049 [P] Update README.md with complete documentation (add project overview, prerequisites (Python 3.12+, UV, Neon database), setup instructions (clone, uv sync, .env config, migrations), how to run API server (uv run uvicorn src.main:app --reload), how to run tests (uv run pytest), API documentation URL (http://localhost:8000/docs), link to specs/ for detailed requirements)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational - Depends on US1 Task model (T021-T022) but independently testable
  - User Story 3 (P3): Can start after Foundational - Depends on US1 Task model (T021-T022) but independently testable
- **Polish (Phase 6)**: Depends on all user stories being complete

### Within Each User Story (TDD Workflow)

1. **Tests FIRST**: Write all test tasks marked [P] in parallel (T015-T020 for US1, T031-T035 for US2, T040-T042 for US3)
2. **Verify RED**: Run tests, ensure they FAIL (proving they test something meaningful)
3. **Models**: Implement data models (T021-T022 for US1)
4. **Schemas**: Implement API contracts (T023 for US1)
5. **Services**: Implement business logic (T024-T026 for US1, T036 for US2, T043 for US3)
6. **Endpoints**: Implement HTTP routes (T027-T029 for US1, T037-T039 for US2, T043 for US3)
7. **Integration**: Wire up to main app (T030 for US1)
8. **Verify GREEN**: Run tests, ensure they PASS
9. **Refactor**: Improve code quality while keeping tests green
10. **Checkpoint**: Validate story independently before moving to next

### User Story Dependencies

- **User Story 1 (P1)**: ✅ No dependencies on other stories
- **User Story 2 (P2)**: ⚠️ Depends on User Story 1 Task model (T021-T022) but can run in parallel after those complete
- **User Story 3 (P3)**: ⚠️ Depends on User Story 1 Task model (T021-T022) but can run in parallel after those complete

### Parallel Opportunities

- **Phase 1 Setup**: All tasks (T001-T003) can run in parallel
- **Phase 2 Foundational**: Tasks marked [P] (T007-T014) can run in parallel after T004-T006 complete (database setup must be sequential)
- **Phase 3 US1 Tests**: All test tasks (T015-T020) can be written in parallel
- **Phase 3 US1 Implementation**: T021-T023 can run in parallel (model split allows T021 first, then T022 adds validation)
- **Phase 3 US1 Services**: T024-T025 can run in parallel (different methods)
- **Phase 4 US2 Tests**: All test tasks (T031-T035) can be written in parallel
- **Phase 5 US3 Tests**: All test tasks (T040-T042) can be written in parallel
- **Phase 6 Polish**: T044-T045 (unit tests), T048-T049 (quality and docs) can run in parallel

**Multi-Developer Strategy**: After Foundational phase completes and T021-T022 finish:
- Developer A: Complete User Story 1 (Phase 3)
- Developer B: User Story 2 (Phase 4) - starts after T021-T022 complete
- Developer C: User Story 3 (Phase 5) - starts after T021-T022 complete

---

## Parallel Example: User Story 1

```bash
# TDD Red Phase: Launch all tests for User Story 1 together
Task: "Write contract test for Task model creation with valid data in tests/contract/test_task_model.py"
Task: "Write contract test for Task model validation failures in tests/contract/test_task_model.py"
Task: "Write integration test for POST /tasks endpoint in tests/integration/test_task_workflows.py"
Task: "Write integration test for GET /tasks/{id} endpoint in tests/integration/test_task_workflows.py"
Task: "Write integration test for GET /tasks list endpoint in tests/integration/test_task_workflows.py"
Task: "Write integration test for GET /tasks filtering in tests/integration/test_task_workflows.py"

# Verify tests FAIL (Red Phase)
uv run pytest tests/ -v -k US1  # Should fail - no implementation yet

# TDD Green Phase: Implement in sequence
# First: Model base structure (enables all other work)
Task: "Create Task model base structure in src/models/task.py"

# Then in parallel: Model validation + API schemas
Task: "Add TaskStatus and TaskPriority enums and validation rules in src/models/task.py"
Task: "Create API request/response schemas in src/api/schemas/task.py"

# Then in parallel: Service methods
Task: "Implement create_task method in src/services/task_service.py"
Task: "Implement get_task_by_id method in src/services/task_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (~1 hour)
2. Complete Phase 2: Foundational (~5 hours) - CRITICAL: blocks all stories
3. Complete Phase 3: User Story 1 (~6.5 hours)
   - Write tests FIRST (T015-T020) - verify they FAIL
   - Implement (T021-T030) - verify tests PASS
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo MVP with create and retrieve functionality

**Total MVP Time**: ~12.5 hours of focused work

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (~6 hours)
2. Add User Story 1 → Test independently → Deploy/Demo (~6.5 hours) - **MVP!**
3. Add User Story 2 → Test independently → Deploy/Demo (~3 hours)
4. Add User Story 3 → Test independently → Deploy/Demo (~1.5 hours)
5. Polish & validate → Final release (~2.5 hours)

**Total Time**: ~19.5 hours of focused work for complete feature

### Parallel Team Strategy

With 3 developers after Foundational phase completes:

1. **All team**: Complete Setup + Foundational together (~6 hours)
2. **Parallel development** (after Foundational):
   - Developer A: User Story 1 (T015-T030) - ~6.5 hours
   - Developer B: Waits for T021-T022, then User Story 2 (T031-T039) - ~3 hours
   - Developer C: Waits for T021-T022, then User Story 3 (T040-T043) - ~1.5 hours
3. **All team**: Polish & validation together (~2.5 hours)

**Total Team Time**: ~9-10 hours with 3 developers (vs 19.5 hours solo)

---

## Notes

- **Task Sizing**: Each task scoped for 20-30 minutes of focused work (revised from v1.0 for better granularity)
- **TDD Workflow**: Tests MUST be written first (Red), implementation second (Green), then refactor
- **[P] tasks**: Different files, no dependencies, can run in parallel
- **[Story] label**: Maps task to specific user story for traceability
- **Independent Stories**: Each user story should be independently completable and testable
- **Verify Tests Fail**: Before implementing, run tests to confirm they fail (Red phase)
- **Commit Strategy**: Commit after each task or when tests go from Red to Green
- **Checkpoints**: Stop at each checkpoint to validate story independently
- **Database Migrations**: Alembic handles schema changes (T005-T006)
- **Error Handling**: Global exception handlers provide consistent error responses (T011)
- **Settings Management**: Environment variables loaded via pydantic-settings (T014)

---

## Task Count Summary

- **Setup**: 3 tasks (~1 hour)
- **Foundational**: 11 tasks (~5 hours) - EXPANDED for completeness
- **User Story 1**: 16 tasks (~6.5 hours) - 6 tests + 10 implementation (model split, service split)
- **User Story 2**: 9 tasks (~3 hours) - 5 tests + 4 implementation (logging integrated)
- **User Story 3**: 4 tasks (~1.5 hours) - 3 tests + 1 implementation (combined)
- **Polish**: 6 tasks (~2.5 hours)

**Total**: 49 tasks, ~19.5 hours estimated

**Parallel Opportunities**: 26 tasks marked [P] can run in parallel within their phases (increased from 18)

**MVP Scope**: Setup + Foundational + User Story 1 = 30 tasks (~12.5 hours)

---

## Changes from v1.0

### Improvements
- ✅ Split oversized tasks: T016 → T021+T022 (model), T018 → T024+T025+T026 (service), T007 → T009+T010 (FastAPI)
- ✅ Combined tiny tasks: T038+T039+T040 → T043 (delete), T022+T023 → T030 (integration)
- ✅ Added missing infrastructure: Alembic migrations (T005-T006), error schemas (T008), exception handlers (T011), settings module (T014)
- ✅ Removed redundancy: Per-story test verification tasks (old T023, T034, T041) replaced by comprehensive Phase 6 validation
- ✅ Better TDD flow: Model split allows testing base before validation, service split enables incremental coverage
- ✅ Clearer sizing: All tasks now genuinely 20-30 minutes with no outliers

### Impact
- Task count: 47 → 49 (+2 tasks)
- Total time: 15.5 → 19.5 hours (+4 hours for infrastructure and better granularity)
- Parallel tasks: 18 → 26 (+8 more parallelizable tasks)
- MVP time: 9 → 12.5 hours (+3.5 hours for more thorough foundation)
