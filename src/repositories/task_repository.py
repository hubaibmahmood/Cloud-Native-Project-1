"""Task repository - Data access layer for task CRUD operations.

This module handles all database queries and operations for tasks.
NO business logic should exist here - only data access.
"""

from typing import Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.api.schemas.task import TaskCreate, TaskUpdate
from src.models.task import Task, TaskPriority, TaskStatus


class TaskRepository:
    """Repository for task data access operations.

    Responsibilities:
    - Execute database queries
    - CRUD operations for tasks
    - NO business logic
    - NO HTTP concerns

    Args:
        db: Async database session
    """

    def __init__(self, db: AsyncSession):
        """Initialize repository with database session.

        Args:
            db: Async database session injected via dependency
        """
        self.db = db

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID.

        Args:
            task_id: Task identifier

        Returns:
            Task if found, None otherwise
        """
        query = select(Task).where(Task.id == task_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        tag: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Task], int]:
        """Retrieve all tasks with optional filtering and pagination.

        Args:
            status: Filter by status (optional)
            priority: Filter by priority (optional)
            tag: Filter by tag (optional)
            limit: Maximum number of tasks to return
            offset: Number of tasks to skip

        Returns:
            Tuple of (tasks list, total count)
        """
        # Build base query
        query = select(Task)

        # Apply filters
        if status is not None:
            query = query.where(Task.status == status)

        if priority is not None:
            query = query.where(Task.priority == priority)

        if tag is not None:
            # PostgreSQL array contains vs SQLite JSON contains
            # Check database dialect
            from sqlalchemy import cast, String

            dialect_name = self.db.bind.dialect.name if self.db.bind else "sqlite"

            if dialect_name == "postgresql":
                # PostgreSQL ARRAY contains
                query = query.where(Task.tags.contains([tag]))
            else:
                # SQLite JSON - search for tag in JSON string
                query = query.where(cast(Task.tags, String).like(f'%"{tag}"%'))

        # Get total count (before pagination)
        count_result = await self.db.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = count_result.scalar_one()

        # Apply pagination and ordering
        query = query.order_by(Task.created_at.desc()).offset(offset).limit(limit)

        # Execute query
        result = await self.db.execute(query)
        tasks = result.scalars().all()

        return list(tasks), total

    async def create(self, task_data: TaskCreate) -> Task:
        """Create a new task.

        Args:
            task_data: Task creation data

        Returns:
            Created task with generated ID
        """
        # Create task instance from schema
        task = Task.model_validate(task_data)

        # Save to database
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def update(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """Update an existing task.

        Args:
            task_id: Task identifier
            task_data: Fields to update

        Returns:
            Updated task if found, None otherwise
        """
        # Get existing task
        task = await self.get_by_id(task_id)
        if not task:
            return None

        # Apply updates (only fields that are set)
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Increment version for optimistic locking
        task.version += 1

        # Update timestamp
        from datetime import UTC, datetime

        task.updated_at = datetime.now(UTC)

        # Save changes
        await self.db.commit()
        await self.db.refresh(task)

        return task

    async def delete(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: Task identifier

        Returns:
            True if deleted, False if not found
        """
        task = await self.get_by_id(task_id)
        if not task:
            return False

        await self.db.delete(task)
        await self.db.commit()

        return True

    async def count(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> int:
        """Count tasks with optional filtering.

        Args:
            status: Filter by status (optional)
            priority: Filter by priority (optional)

        Returns:
            Total count of matching tasks
        """
        query = select(func.count(Task.id))

        if status is not None:
            query = query.where(Task.status == status)

        if priority is not None:
            query = query.where(Task.priority == priority)

        result = await self.db.execute(query)
        return result.scalar_one()
