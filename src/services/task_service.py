"""Task service - Business logic for task operations.

This module contains business rules, validation, and orchestration.
It uses the repository layer for data access.
"""

from typing import Optional

from fastapi import HTTPException, status

from src.api.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from src.models.task import TaskPriority, TaskStatus
from src.repositories.task_repository import TaskRepository
from src.utils.logging import logger


class TaskService:
    """Service for task business logic.

    Responsibilities:
    - Apply business rules and validation
    - Orchestrate repository calls
    - Handle domain-level errors
    - Transaction coordination
    - NO HTTP concerns (no HTTPException for routes)
    - NO database queries (use repository)

    Args:
        repository: Task repository for data access
    """

    def __init__(self, repository: TaskRepository):
        """Initialize service with repository.

        Args:
            repository: Task repository injected via dependency
        """
        self.repository = repository

    async def create_task(self, task_data: TaskCreate) -> TaskResponse:
        """Create a new task.

        Business logic:
        - Validate task data (handled by Pydantic)
        - Create task via repository
        - Log creation event

        Args:
            task_data: Task creation data

        Returns:
            Created task as response model

        Raises:
            HTTPException: If creation fails (for now, will use domain exceptions later)
        """
        try:
            # Create task via repository
            task = await self.repository.create(task_data)

            logger.info(f"Created task {task.id}: {task.title}")

            return TaskResponse.model_validate(task)

        except Exception as e:
            logger.error(f"Failed to create task: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create task",
            ) from e

    async def get_task(self, task_id: int) -> TaskResponse:
        """Get task by ID.

        Business logic:
        - Retrieve task from repository
        - Raise error if not found

        Args:
            task_id: Task identifier

        Returns:
            Task as response model

        Raises:
            HTTPException: If task not found (404)
        """
        task = await self.repository.get_by_id(task_id)

        if task is None:
            logger.debug(f"Task {task_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found",
            )

        logger.debug(f"Retrieved task {task_id}")
        return TaskResponse.model_validate(task)

    async def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        tag: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[TaskResponse], int]:
        """List all tasks with optional filtering.

        Business logic:
        - Apply pagination limits
        - Filter by status/priority/tag
        - Return tasks and total count

        Args:
            status: Filter by status (optional)
            priority: Filter by priority (optional)
            tag: Filter by tag (optional)
            limit: Maximum tasks to return (default: 50)
            offset: Number of tasks to skip (default: 0)

        Returns:
            Tuple of (task list, total count)
        """
        tasks, total = await self.repository.get_all(
            status=status,
            priority=priority,
            tag=tag,
            limit=limit,
            offset=offset,
        )

        logger.info(
            f"Retrieved {len(tasks)} tasks (total: {total}, "
            f"filters: status={status}, priority={priority}, tag={tag})"
        )

        # Convert to response models
        task_responses = [TaskResponse.model_validate(task) for task in tasks]

        return task_responses, total

    async def update_task(
        self,
        task_id: int,
        task_data: TaskUpdate,
        current_version: Optional[int] = None,
    ) -> TaskResponse:
        """Update an existing task.

        Business logic:
        - Check task exists
        - Validate version for optimistic locking (if provided)
        - Apply updates via repository
        - Log update event

        Args:
            task_id: Task identifier
            task_data: Fields to update
            current_version: Expected version for optimistic locking (optional)

        Returns:
            Updated task as response model

        Raises:
            HTTPException: If task not found (404) or version conflict (409)
        """
        # Check if task exists
        existing_task = await self.repository.get_by_id(task_id)

        if existing_task is None:
            logger.debug(f"Task {task_id} not found for update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found",
            )

        # Check version for optimistic locking
        if current_version is not None and existing_task.version != current_version:
            logger.warning(
                f"Version conflict for task {task_id}: "
                f"current={existing_task.version}, requested={current_version}"
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "VERSION_CONFLICT",
                    "message": "Task has been modified by another request",
                    "current_version": existing_task.version,
                    "requested_version": current_version,
                },
            )

        # Update task via repository
        updated_task = await self.repository.update(task_id, task_data)

        if updated_task is None:
            logger.error(f"Failed to update task {task_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update task",
            )

        logger.info(f"Updated task {task_id}")

        return TaskResponse.model_validate(updated_task)

    async def delete_task(self, task_id: int) -> None:
        """Delete a task.

        Business logic:
        - Check task exists
        - Delete via repository
        - Log deletion event

        Args:
            task_id: Task identifier

        Raises:
            HTTPException: If task not found (404)
        """
        # Check if task exists
        existing_task = await self.repository.get_by_id(task_id)

        if existing_task is None:
            logger.debug(f"Task {task_id} not found for deletion")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found",
            )

        # Delete via repository
        success = await self.repository.delete(task_id)

        if not success:
            logger.error(f"Failed to delete task {task_id}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete task",
            )

        logger.info(f"Deleted task {task_id}")
