"""Task model with SQLModel for database and validation."""

from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum

from pydantic import field_validator
from sqlalchemy import ARRAY, Column, JSON, String, TIMESTAMP
from sqlalchemy.types import DateTime
from sqlmodel import Field, SQLModel


class TaskStatus(str, Enum):
    """Valid task status values."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    """Valid task priority levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task(SQLModel, table=True):
    """Task entity representing a work item.

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

    # Primary key
    id: int | None = Field(default=None, primary_key=True)

    # Required fields
    title: str = Field(min_length=1, max_length=200)

    # Optional fields
    description: str | None = Field(default=None, max_length=5000)

    # Enum fields with defaults
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)

    # Date/time fields
    due_date: datetime | None = Field(
        default=None,
        sa_type=DateTime(timezone=True),  # PostgreSQL TIMESTAMP WITH TIME ZONE
    )

    # Array field (PostgreSQL ARRAY type, JSON for SQLite)
    tags: list[str] = Field(
        default_factory=list,
        sa_column=Column(
            ARRAY(String(50)).with_variant(JSON, "sqlite"),
        ),
    )

    # Numeric field
    estimated_hours: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    # System-managed fields
    version: int = Field(default=1, ge=1)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_type=DateTime(timezone=True),  # PostgreSQL TIMESTAMP WITH TIME ZONE
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_type=DateTime(timezone=True),  # PostgreSQL TIMESTAMP WITH TIME ZONE
    )

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title is not empty and within length limits."""
        if not v or len(v.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(v) > 200:
            raise ValueError("Title must not exceed 200 characters")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str | None) -> str | None:
        """Validate description length."""
        if v is not None and len(v) > 5000:
            raise ValueError("Description must not exceed 5000 characters")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tag_length(cls, v: list[str]) -> list[str]:
        """Validate that each tag does not exceed 50 characters."""
        for tag in v:
            if len(tag) > 50:
                raise ValueError("Tag must not exceed 50 characters")
        return v

    @field_validator("estimated_hours")
    @classmethod
    def validate_estimated_hours(cls, v: Decimal | None) -> Decimal | None:
        """Validate estimated_hours is non-negative."""
        if v is not None and v < 0:
            raise ValueError("Estimated hours must be non-negative")
        return v

    model_config = {
        "validate_assignment": True,
        "str_strip_whitespace": False,  # Don't auto-strip to catch empty strings
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
                "updated_at": "2026-01-08T10:30:00Z",
            }
        },
    }
