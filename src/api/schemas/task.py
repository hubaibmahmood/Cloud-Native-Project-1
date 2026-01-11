"""API request/response schemas for Task endpoints."""

from datetime import datetime
from decimal import Decimal

from pydantic import Field
from sqlmodel import SQLModel

from src.models.task import TaskPriority, TaskStatus


class TaskCreate(SQLModel):
    """Schema for creating a new task.

    Only includes fields that can be set by the user.
    System fields (id, version, timestamps) are auto-generated.
    """

    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: datetime | None = None
    tags: list[str] = Field(default_factory=list)
    estimated_hours: Decimal | None = Field(default=None, ge=0)


class TaskUpdate(SQLModel):
    """Schema for updating an existing task.

    All fields are optional to support partial updates.
    """

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None
    tags: list[str] | None = None
    estimated_hours: Decimal | None = Field(default=None, ge=0)


class TaskResponse(SQLModel):
    """Schema for task responses.

    Includes all task fields including system-managed ones.
    """

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None
    tags: list[str]
    estimated_hours: Decimal | None
    version: int
    created_at: datetime
    updated_at: datetime


class TaskList(SQLModel):
    """Schema for paginated task list responses."""

    tasks: list[TaskResponse]
    total: int
    limit: int
    offset: int
