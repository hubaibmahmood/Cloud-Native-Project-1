"""Dependency injection for FastAPI routes.

This module provides the dependency injection chain:
Database Session → Repository → Service → Route

Benefits:
- Loose coupling between layers
- Easy testing (can override dependencies)
- Clear dependency graph
- Automatic cleanup (async context managers)
"""


from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import get_db
from src.repositories.task_repository import TaskRepository
from src.services.task_service import TaskService


# Repository Dependencies


def get_task_repository(
    db: AsyncSession = Depends(get_db),
) -> TaskRepository:
    """Get task repository with database session.

    This creates a TaskRepository instance with the injected database session.
    The repository will be created fresh for each request.

    Args:
        db: Database session (injected)

    Returns:
        TaskRepository instance
    """
    return TaskRepository(db)


# Service Dependencies


def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    """Get task service with repository.

    This creates a TaskService instance with the injected repository.
    The service will be created fresh for each request.

    Dependency chain: db → repository → service

    Args:
        repository: Task repository (injected)

    Returns:
        TaskService instance
    """
    return TaskService(repository)


# Example of how to use in routes:
# @router.post("/tasks")
# async def create_task(
#     task_data: TaskCreate,
#     service: TaskService = Depends(get_task_service)
# ):
#     return await service.create_task(task_data)
