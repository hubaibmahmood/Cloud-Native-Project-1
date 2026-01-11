"""Task API endpoints - CRUD operations for tasks (v1).

This module follows Clean Architecture principles:
- Routes handle HTTP requests/responses ONLY
- NO business logic in routes
- NO database queries in routes
- All logic delegated to service layer
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from src.api.dependencies import get_task_service
from src.api.schemas.task import TaskCreate, TaskList, TaskResponse, TaskUpdate
from src.models.task import TaskPriority, TaskStatus
from src.services.task_service import TaskService

# Create router for task endpoints
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Task not found"}},
)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    response_description="The created task",
    responses={
        201: {"description": "Task created successfully"},
        400: {"description": "Invalid request data"},
        422: {"description": "Validation error"},
    },
)
async def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Create a new task with provided data.

    - **title**: Required, max 200 characters
    - **description**: Optional, max 5000 characters
    - **status**: Defaults to 'pending'
    - **priority**: Defaults to 'medium'
    - **due_date**: Optional ISO 8601 datetime
    - **tags**: Optional array of strings (max 50 chars each)
    - **estimated_hours**: Optional non-negative decimal

    Returns the created task with generated ID and timestamps.
    """
    return await service.create_task(task_data)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
    response_description="The requested task",
    responses={
        200: {"description": "Task found"},
        404: {"description": "Task not found"},
    },
)
async def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Retrieve a task by its ID.

    Returns 404 if task does not exist.
    """
    return await service.get_task(task_id)


@router.get(
    "/",
    response_model=TaskList,
    summary="List all tasks with optional filtering",
    response_description="Paginated list of tasks",
    responses={
        200: {"description": "Tasks retrieved successfully"},
    },
)
async def list_tasks(
    status_filter: Optional[TaskStatus] = Query(
        None, alias="status", description="Filter by task status"
    ),
    priority_filter: Optional[TaskPriority] = Query(
        None, alias="priority", description="Filter by task priority"
    ),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    limit: int = Query(50, ge=1, le=100, description="Maximum tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip"),
    service: TaskService = Depends(get_task_service),
) -> TaskList:
    """List all tasks with optional filtering and pagination.

    **Filters**:
    - **status**: Filter by task status (pending, in_progress, completed)
    - **priority**: Filter by priority (critical, high, medium, low)
    - **tag**: Filter by tag (returns tasks containing this tag)

    **Pagination**:
    - **limit**: Maximum number of tasks to return (1-100, default: 50)
    - **offset**: Number of tasks to skip (default: 0)

    Returns paginated task list with total count and metadata.
    """
    tasks, total = await service.list_tasks(
        status=status_filter,
        priority=priority_filter,
        tag=tag,
        limit=limit,
        offset=offset,
    )

    return TaskList(
        tasks=tasks,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update an existing task",
    response_description="The updated task",
    responses={
        200: {"description": "Task updated successfully"},
        404: {"description": "Task not found"},
        409: {"description": "Version conflict (optimistic locking)"},
        422: {"description": "Validation error"},
    },
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    if_match: Optional[int] = Query(
        None,
        alias="If-Match",
        description="Version number for optimistic locking",
    ),
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Update a task (partial update).

    Supports optimistic locking via If-Match header with version number.
    Only provided fields will be updated.

    Returns 409 Conflict if version mismatch detected.
    """
    return await service.update_task(task_id, task_data, current_version=if_match)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    responses={
        204: {"description": "Task deleted successfully"},
        404: {"description": "Task not found"},
    },
)
async def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> None:
    """Delete a task by its ID.

    Returns 204 No Content on successful deletion.
    Returns 404 if task does not exist.
    """
    await service.delete_task(task_id)
