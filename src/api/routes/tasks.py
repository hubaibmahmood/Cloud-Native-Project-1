"""Task API endpoints - CRUD operations for tasks."""

from fastapi import APIRouter, Depends, Query, status

from src.api.dependencies import get_task_service
from src.api.schemas.task import TaskCreate, TaskList, TaskResponse
from src.models.task import TaskPriority, TaskStatus
from src.services.task_service import TaskService

# Create router for task endpoints
router = APIRouter()


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    responses={
        201: {"description": "Task created successfully"},
        400: {"description": "Invalid request data"},
        422: {"description": "Validation error"},
    },
)
async def create_task_endpoint(
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
    """
    return await service.create_task(task_data)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
    responses={
        200: {"description": "Task found"},
        404: {"description": "Task not found"},
    },
)
async def get_task_endpoint(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    """Retrieve a task by its ID.

    Returns 404 if task does not exist.
    """
    return await service.get_task(task_id)


@router.get(
    "",
    response_model=TaskList,
    summary="List all tasks with optional filtering",
    responses={
        200: {"description": "Tasks retrieved successfully"},
    },
)
async def list_tasks_endpoint(
    status_filter: TaskStatus | None = Query(None, alias="status"),
    priority_filter: TaskPriority | None = Query(None, alias="priority"),
    tag: str | None = Query(None, description="Filter by tag"),
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
    """
    task_responses, total = await service.list_tasks(
        status=status_filter,
        priority=priority_filter,
        tag=tag,
        limit=limit,
        offset=offset,
    )

    return TaskList(
        tasks=task_responses,
        total=total,
        limit=limit,
        offset=offset,
    )
