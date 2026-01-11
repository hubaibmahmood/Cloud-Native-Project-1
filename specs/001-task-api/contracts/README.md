# API Contracts

This directory contains API contract specifications for the Task Management API.

## Files

### openapi.yaml
OpenAPI 3.1.0 specification defining all REST endpoints, request/response schemas, and error formats.

**View the documentation**:
- Copy `openapi.yaml` to [Swagger Editor](https://editor.swagger.io/)
- Or run locally: `npx @redocly/cli preview-docs openapi.yaml`

## Endpoints Summary

| Method | Path | Description | Status Codes |
|--------|------|-------------|--------------|
| GET | /tasks | List all tasks (with filtering/pagination) | 200, 400, 500 |
| POST | /tasks | Create a new task | 201, 400, 422, 500 |
| GET | /tasks/{task_id} | Get a specific task | 200, 404, 500 |
| PATCH | /tasks/{task_id} | Update a task (requires If-Match header) | 200, 400, 404, 409, 412, 422, 500 |
| DELETE | /tasks/{task_id} | Delete a task | 204, 404, 500 |

## Key Patterns

### Optimistic Locking (PATCH /tasks/{task_id})
- Client includes current version in `If-Match` header
- Server validates version matches database
- On mismatch: returns 409 Conflict with current version
- On success: increments version and returns updated task

**Example**:
```http
PATCH /tasks/1 HTTP/1.1
Content-Type: application/json
If-Match: "3"

{
  "status": "completed"
}
```

**Success (200 OK)**:
```json
{
  "id": 1,
  "title": "Complete report",
  "status": "completed",
  "version": 4,
  "..."
}
```

**Conflict (409 Conflict)**:
```json
{
  "error": {
    "code": "VERSION_CONFLICT",
    "message": "Task was modified by another request. Current version is 5.",
    "current_version": 5,
    "requested_version": 3
  }
}
```

### Error Response Format
All errors follow consistent structure:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "details": []  // Optional: field-level errors
  }
}
```

### Validation Errors (422)
Pydantic validation failures return field-level details:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      {
        "field": "title",
        "issue": "Field required"
      },
      {
        "field": "description",
        "issue": "String should have at most 5000 characters"
      }
    ]
  }
}
```

## Testing the API

### Using curl
```bash
# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "This is a test"}'

# Get all tasks
curl http://localhost:8000/tasks

# Get a specific task
curl http://localhost:8000/tasks/1

# Update a task (with version)
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -H "If-Match: 1" \
  -d '{"status": "completed"}'

# Delete a task
curl -X DELETE http://localhost:8000/tasks/1
```

### Using httpx (Python)
```python
import httpx

async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
    # Create task
    response = await client.post("/tasks", json={
        "title": "Test task",
        "description": "This is a test"
    })
    task = response.json()

    # Update task with optimistic locking
    response = await client.patch(
        f"/tasks/{task['id']}",
        headers={"If-Match": str(task['version'])},
        json={"status": "completed"}
    )
```

## Contract Validation

The OpenAPI specification serves as the source of truth for:
- Request/response schemas
- Validation rules (min/max length, required fields)
- HTTP status codes
- Error response formats

FastAPI generates this documentation automatically from code, but this static spec:
- Documents the intended design before implementation
- Serves as a contract for API consumers
- Enables contract testing (validate implementation matches spec)
- Supports API client generation (OpenAPI Generator, etc.)

## References

- [OpenAPI 3.1.0 Specification](https://spec.openapis.org/oas/v3.1.0)
- [FastAPI OpenAPI Documentation](https://fastapi.tiangolo.com/tutorial/metadata/)
- [Swagger Editor](https://editor.swagger.io/)
