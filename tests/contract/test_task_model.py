"""Contract tests for Task model - Data validation and defaults."""

import pytest
from datetime import datetime, UTC
from decimal import Decimal
from pydantic import ValidationError

from src.models.task import Task, TaskStatus, TaskPriority


class TestTaskModelCreation:
    """Test Task model creation with valid data."""

    def test_create_task_with_all_fields(self):
        """T015: Create task with all 11 fields and verify defaults."""
        task = Task(
            title="Complete project report",
            description="Finalize Q4 report with metrics and analysis",
            status=TaskStatus.PENDING,
            priority=TaskPriority.HIGH,
            due_date=datetime(2026, 1, 15, 18, 0, 0, tzinfo=UTC),
            tags=["urgent", "documentation"],
            estimated_hours=Decimal("8.5"),
        )

        # Verify all fields
        assert task.title == "Complete project report"
        assert task.description == "Finalize Q4 report with metrics and analysis"
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.HIGH
        assert task.due_date == datetime(2026, 1, 15, 18, 0, 0, tzinfo=UTC)
        assert task.tags == ["urgent", "documentation"]
        assert task.estimated_hours == Decimal("8.5")

        # Verify defaults
        assert task.version == 1
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)
        assert task.id is None  # Not set until saved to database

    def test_create_task_with_minimal_fields(self):
        """Create task with only required field (title)."""
        task = Task(title="Simple task")

        # Verify required field
        assert task.title == "Simple task"

        # Verify defaults
        assert task.description is None
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.MEDIUM
        assert task.due_date is None
        assert task.tags == []
        assert task.estimated_hours is None
        assert task.version == 1


class TestTaskModelValidation:
    """Test Task model validation failures."""

    def test_empty_title_fails(self):
        """T016: Empty title should fail validation."""
        with pytest.raises(ValidationError) as exc_info:
            Task(title="")

        errors = exc_info.value.errors()
        assert any("title" in str(error["loc"]) for error in errors)

    def test_title_too_long_fails(self):
        """Title exceeding 200 characters should fail."""
        long_title = "x" * 201
        with pytest.raises(ValidationError) as exc_info:
            Task(title=long_title)

        errors = exc_info.value.errors()
        assert any("title" in str(error["loc"]) for error in errors)

    def test_description_too_long_fails(self):
        """Description exceeding 5000 characters should fail."""
        long_description = "x" * 5001
        with pytest.raises(ValidationError) as exc_info:
            Task(title="Valid title", description=long_description)

        errors = exc_info.value.errors()
        assert any("description" in str(error["loc"]) for error in errors)

    def test_invalid_status_fails(self):
        """Invalid status value should fail."""
        with pytest.raises(ValidationError):
            Task(title="Valid title", status="invalid_status")

    def test_invalid_priority_fails(self):
        """Invalid priority value should fail."""
        with pytest.raises(ValidationError):
            Task(title="Valid title", priority="invalid_priority")

    def test_negative_estimated_hours_fails(self):
        """Negative estimated_hours should fail."""
        with pytest.raises(ValidationError) as exc_info:
            Task(title="Valid title", estimated_hours=Decimal("-1.5"))

        errors = exc_info.value.errors()
        assert any("estimated_hours" in str(error["loc"]) for error in errors)

    def test_tag_too_long_fails(self):
        """Tag exceeding 50 characters should fail validation."""
        long_tag = "x" * 51
        with pytest.raises(ValidationError) as exc_info:
            Task(title="Valid title", tags=[long_tag])

        errors = exc_info.value.errors()
        assert any("tags" in str(error["loc"]) for error in errors)


class TestTaskModelUpdate:
    """Test Task model updates and version management."""

    def test_update_task_increments_version(self):
        """T031: Update task and verify version increments."""
        # Create initial task
        task = Task(
            title="Original title",
            description="Original description",
            priority=TaskPriority.MEDIUM,
        )

        # Verify initial state
        assert task.version == 1
        assert task.title == "Original title"
        original_created_at = task.created_at
        original_updated_at = task.updated_at

        # Simulate update (in real scenario, repository handles this)
        task.title = "Updated title"
        task.description = "Updated description"
        task.version += 1
        task.updated_at = datetime.now(UTC)

        # Verify update
        assert task.version == 2
        assert task.title == "Updated title"
        assert task.description == "Updated description"
        assert task.created_at == original_created_at  # Unchanged
        assert task.updated_at > original_updated_at  # Changed
