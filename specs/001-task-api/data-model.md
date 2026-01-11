# Data Model: Task Management API

**Feature**: 001-task-api
**Date**: 2026-01-08
**Status**: Phase 1 Complete

## Purpose

This document defines the data entities, their attributes, validation rules, relationships, and state transitions for the Task Management API.

---

## Entity: Task

The Task entity represents a work item that users can create, view, update, and delete.

### Attributes

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | Integer | PRIMARY KEY, AUTO_INCREMENT | System-generated | Unique identifier for the task |
| `title` | String | NOT NULL, MAX_LENGTH=200 | - | Brief description of the task |
| `description` | String (nullable) | MAX_LENGTH=5000 | NULL | Detailed information about the task |
| `status` | Enum String | NOT NULL, IN('pending', 'in_progress', 'completed') | 'pending' | Current state of the task |
| `priority` | Enum String | NOT NULL, IN('critical', 'high', 'medium', 'low') | 'medium' | Task priority level |
| `due_date` | DateTime (UTC, nullable) | - | NULL | When the task should be completed |
| `tags` | Array of Strings | Each tag MAX_LENGTH=50 | [] | Labels for categorization |
| `estimated_hours` | Decimal (nullable) | >= 0, precision=2 | NULL | Estimated effort in hours |
| `version` | Integer | NOT NULL, >= 1 | 1 | Optimistic locking version number |
| `created_at` | DateTime (UTC) | NOT NULL | System timestamp | When the task was created |
| `updated_at` | DateTime (UTC) | NOT NULL | System timestamp | When the task was last modified |

### Validation Rules

**Title**:
- ❌ Empty string → Reject with 400 "Title is required"
- ❌ Whitespace only → Reject with 400 "Title cannot be blank"
- ❌ Length > 200 characters → Reject with 400 "Title must not exceed 200 characters"
- ✅ Valid: "Complete project report"

**Description**:
- ✅ NULL/omitted → Allowed (optional field)
- ✅ Empty string → Stored as NULL or empty
- ❌ Length > 5000 characters → Reject with 400 "Description must not exceed 5000 characters"
- ✅ Valid: Long text with line breaks, special characters, Unicode

**Status**:
- ✅ One of: "pending", "in_progress", "completed"
- ❌ Any other value → Reject with 400 "Invalid status. Must be one of: pending, in_progress, completed"
- ✅ Defaults to "pending" if not provided during creation

**Priority**:
- ✅ One of: "critical", "high", "medium", "low"
- ❌ Any other value → Reject with 400 "Invalid priority. Must be one of: critical, high, medium, low"
- ✅ Defaults to "medium" if not provided during creation
- ✅ Valid: "critical" (most urgent), "high", "medium", "low" (least urgent)

**Due Date**:
- ✅ NULL/omitted → Allowed (optional field)
- ✅ Valid ISO 8601 datetime → Stored as UTC timestamp
- ❌ Invalid date format → Reject with 400 "Invalid due_date format. Use ISO 8601 (e.g., 2026-01-15T18:00:00Z)"
- ⚠️ Past dates allowed (user may set historical deadlines or overdue tasks)
- ✅ Valid: "2026-01-15T18:00:00Z", "2026-12-31T23:59:59Z", NULL

**Tags**:
- ✅ Empty array [] → Allowed (no tags)
- ✅ NULL/omitted → Stored as empty array []
- ✅ Array of strings → Each tag validated individually
- ❌ Tag length > 50 characters → Reject with 400 "Tag must not exceed 50 characters"
- ❌ Duplicate tags → Optionally deduplicate or reject (to be decided during implementation)
- ✅ Valid: ["bug", "urgent", "backend"], ["feature"], []
- ⚠️ No tag count limit enforced (reasonable use expected)

**Estimated Hours**:
- ✅ NULL/omitted → Allowed (optional field)
- ✅ Positive decimal (>= 0) → Stored with 2 decimal precision
- ❌ Negative value → Reject with 400 "Estimated hours must be non-negative"
- ❌ Non-numeric value → Reject with 400 "Estimated hours must be a number"
- ✅ Valid: 2.5, 8.0, 0.25, NULL
- ⚠️ Zero hours (0.0) allowed (quick tasks)

**Version**:
- System-managed field (not user-settable)
- Initialized to 1 on task creation
- Incremented by 1 on each successful update
- Used for optimistic locking conflict detection

**Timestamps**:
- System-managed fields (not user-settable)
- `created_at`: Set once at creation time, immutable
- `updated_at`: Updated on every modification
- Both stored in UTC using `datetime.now(UTC)` (Python 3.12+ modern API)

### State Transitions

The status field follows these allowed transitions:

```
pending ──────────► in_progress ──────────► completed
   │                     │                      ▲
   │                     │                      │
   └─────────────────────┴──────────────────────┘
         (All transitions are bidirectional)
```

**Allowed Transitions**:
- pending → in_progress (user starts working)
- in_progress → completed (user finishes task)
- completed → in_progress (user reopens task)
- completed → pending (user resets task)
- in_progress → pending (user pauses task)
- pending → completed (user marks as done without intermediate state)

**Implementation Note**: The API does not enforce strict state machine logic. Users can transition between any valid status values. This design follows YAGNI principle - strict enforcement can be added later if business rules require it.

### Database Schema (PostgreSQL)

```sql
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    due_date TIMESTAMP WITH TIME ZONE,
    tags TEXT[],  -- PostgreSQL array of text
    estimated_hours DECIMAL(5, 2),  -- Max 999.99 hours
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT status_values CHECK (status IN ('pending', 'in_progress', 'completed')),
    CONSTRAINT priority_values CHECK (priority IN ('critical', 'high', 'medium', 'low')),
    CONSTRAINT estimated_hours_non_negative CHECK (estimated_hours >= 0)
);

-- Indexes for common query patterns
CREATE INDEX idx_task_status ON task(status);
CREATE INDEX idx_task_priority ON task(priority);
CREATE INDEX idx_task_due_date ON task(due_date) WHERE due_date IS NOT NULL;
CREATE INDEX idx_task_created_at ON task(created_at DESC);
CREATE INDEX idx_task_tags ON task USING GIN(tags);  -- GIN index for array searches
```

### SQLModel Implementation

```python
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import ARRAY, String
from datetime import datetime, UTC
from decimal import Decimal
from enum import Enum

class TaskStatus(str, Enum):
    """Valid task status values"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority(str, Enum):
    """Valid task priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Task(SQLModel, table=True):
    """
    Task entity representing a work item.

    Attributes:
        id: Unique identifier (auto-generated)
        title: Brief task description (required, max 200 chars)
        description: Detailed task information (optional, max 5000 chars)
        status: Current task state (pending/in_progress/completed)
        priority: Task priority level (critical/high/medium/low)
        due_date: When task should be completed (optional)
        tags: Array of labels for categorization (optional)
        estimated_hours: Estimated effort in hours (optional)
        version: Optimistic locking version number
        created_at: Task creation timestamp (UTC)
        updated_at: Last modification timestamp (UTC)
    """
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: datetime | None = Field(default=None)
    tags: list[str] = Field(default=[], sa_column=Column(ARRAY(String(50))))
    estimated_hours: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    version: int = Field(default=1, ge=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    model_config = {
        "json_schema_extra": {
            "example": {
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
        }
    }
```

---

## Relationships

**Current Scope**: No relationships defined. Task is a standalone entity.

**Future Considerations** (out of scope for this feature):
- Task → User (owner/assignee)
- Task → Project (grouping)
- Task → Tags (categorization)
- Task → Comments (collaboration)
- Task → Attachments (file uploads)

Per YAGNI principle, these relationships are not implemented unless explicitly required.

---

## Optimistic Locking Strategy

### Purpose
Prevent lost updates when multiple clients modify the same task concurrently.

### Mechanism
1. Client reads task: receives current version (e.g., version=3)
2. Client modifies task locally
3. Client sends update request with current version number
4. Server checks: `task.version == request.version`
   - **Match**: Apply updates, increment version to 4, return success
   - **Mismatch**: Reject with 409 Conflict, return current state

### API Contract for Updates

**Request** (include current version):
```http
PATCH /tasks/42 HTTP/1.1
Content-Type: application/json
If-Match: "3"

{
  "title": "Updated title",
  "status": "completed"
}
```

**Success Response** (200 OK):
```json
{
  "id": 42,
  "title": "Updated title",
  "status": "completed",
  "version": 4,
  "updated_at": "2026-01-08T15:45:30Z"
}
```

**Conflict Response** (409 Conflict):
```json
{
  "error": {
    "code": "VERSION_CONFLICT",
    "message": "Task was modified by another request. Current version is 4.",
    "current_version": 4,
    "requested_version": 3
  }
}
```

### Client Handling
1. **On 409 Conflict**: Re-fetch task, merge changes (if possible), retry with new version
2. **Retry Logic**: Implement exponential backoff (avoid tight retry loops)
3. **User Feedback**: Inform user about conflict and show current state

---

## Edge Cases and Handling

### 1. Concurrent Creation
**Scenario**: Multiple clients create tasks with same title simultaneously
**Handling**: Allowed - each gets unique ID. Titles are not unique constraints.

### 2. Delete During Update
**Scenario**: Client A updates task, Client B deletes it concurrently
**Handling**:
- If delete happens first: Update returns 404 Not Found
- If update happens first: Delete succeeds, update was applied

### 3. Version Overflow
**Scenario**: Task version exceeds integer limit (unlikely: 2.1B updates)
**Handling**: Not explicitly handled. PostgreSQL integer type supports 2^31-1 updates.

### 4. Timestamp Precision
**Scenario**: Two updates occur in same millisecond
**Handling**: Version field is authoritative, not timestamps. Timestamps are for audit only.

### 5. Malformed Data
**Scenario**: Client sends invalid JSON, wrong types, missing required fields
**Handling**:
- Pydantic validation rejects before business logic
- Return 422 Unprocessable Entity with field-level errors

### 6. Special Characters in Text
**Scenario**: Title/description contains emojis, newlines, control characters
**Handling**: Allow all Unicode. PostgreSQL TEXT type supports full UTF-8.

### 7. Soft vs Hard Delete
**Decision**: Hard delete (permanent removal)
**Rationale**: Spec states "Task deletion is permanent" (Assumptions section)
**Implementation**: `DELETE FROM task WHERE id = ?`

---

## Data Migration Plan

### Initial Schema Creation
```bash
# Using Alembic or SQLModel's create_all
uv run alembic init migrations
uv run alembic revision --autogenerate -m "Create task table"
uv run alembic upgrade head
```

### Schema Changes (Future)
All schema modifications must:
1. Be backward compatible (or include migration path)
2. Preserve existing data
3. Include rollback script
4. Be tested in non-production first

---

## Performance Considerations

### Indexes
- **Primary Key (id)**: Automatic B-tree index for lookups
- **status**: Index for filtering (e.g., "show all pending tasks")
- **created_at**: Index for chronological sorting (DESC for "newest first")

### Query Patterns
- **Frequent**: GET by ID (O(1) via PK), list all tasks
- **Moderate**: Filter by status, sort by created_at
- **Rare**: Full-text search (not indexed in v1)

### Scaling Strategy
- **Connection Pooling**: Neon provides this, set min/max pool size
- **Pagination**: Implement offset/limit (50 items default per spec)
- **Caching**: Not in v1 scope (add if read latency exceeds budget)

---

## Testing Requirements

### Contract Tests (tests/contract/test_task_model.py)
- ✅ Task creation with valid data succeeds
- ✅ Task creation with missing title fails
- ✅ Task creation with title > 200 chars fails
- ✅ Task creation with description > 5000 chars fails
- ✅ Task creation with invalid status fails
- ✅ Task creation defaults status to "pending"
- ✅ Task creation sets timestamps automatically
- ✅ Task creation initializes version to 1

### Integration Tests (tests/integration/test_task_workflows.py)
- ✅ Create task → Retrieve task (data matches)
- ✅ Create task → Update task → Version increments
- ✅ Create task → Delete task → Retrieval fails with 404
- ✅ Concurrent updates trigger version conflict (409)

### Unit Tests (tests/unit/test_task_service.py)
- ✅ Optimistic locking logic detects version mismatch
- ✅ Validation helper functions reject invalid data

---

## Summary

**Entity Count**: 1 (Task)
**Relationships**: 0 (standalone entity)
**Key Design Patterns**:
- Optimistic locking via version field
- System-managed timestamps and IDs
- Enum-based status validation
- Nullable description for flexibility

**Alignment**:
- ✅ Functional Requirements: FR-001 through FR-019
- ✅ Success Criteria: SC-001 through SC-012
- ✅ Constitution: Type safety, validation, modern APIs
- ✅ YAGNI: No unnecessary fields or relationships

**Next Steps**:
- Generate API contracts (OpenAPI schema in contracts/)
- Create quickstart.md for developer onboarding
