"""Integration tests for Task API workflows - End-to-end user scenarios."""

import pytest
from httpx import AsyncClient


class TestCreateTask:
    """Test POST /tasks endpoint."""

    @pytest.mark.asyncio
    async def test_create_task_with_all_fields(self, client: AsyncClient):
        """T017: Create task with all fields and verify 201 response."""
        task_data = {
            "title": "Complete project report",
            "description": "Finalize Q4 report with metrics and analysis",
            "status": "pending",
            "priority": "high",
            "due_date": "2026-01-15T18:00:00Z",
            "tags": ["urgent", "documentation"],
            "estimated_hours": 8.5,
        }

        response = await client.post("/api/v1/tasks/", json=task_data)

        # Verify 201 Created
        assert response.status_code == 201

        # Verify response data
        data = response.json()
        assert data["id"] is not None
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert data["priority"] == task_data["priority"]
        assert data["tags"] == task_data["tags"]
        # estimated_hours is returned as string from Decimal
        assert float(data["estimated_hours"]) == task_data["estimated_hours"]
        assert data["version"] == 1
        assert "created_at" in data
        assert "updated_at" in data

    @pytest.mark.asyncio
    async def test_create_task_with_minimal_fields(self, client: AsyncClient):
        """Create task with only required field (title)."""
        task_data = {"title": "Simple task"}

        response = await client.post("/api/v1/tasks/", json=task_data)

        # Verify 201 Created
        assert response.status_code == 201

        # Verify defaults
        data = response.json()
        assert data["title"] == "Simple task"
        assert data["description"] is None
        assert data["status"] == "pending"
        assert data["priority"] == "medium"
        assert data["tags"] == []
        assert data["version"] == 1


class TestGetTask:
    """Test GET /tasks/{id} endpoint."""

    @pytest.mark.asyncio
    async def test_get_task_by_id(self, client: AsyncClient):
        """T018: Create task, retrieve by ID, verify data matches."""
        # Create task
        task_data = {
            "title": "Test task",
            "description": "Test description",
            "priority": "high",
        }
        create_response = await client.post("/api/v1/tasks/", json=task_data)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Retrieve task
        response = await client.get(f"/api/v1/tasks/{task_id}")

        # Verify 200 OK
        assert response.status_code == 200

        # Verify data matches
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["priority"] == task_data["priority"]

    @pytest.mark.asyncio
    async def test_get_nonexistent_task_returns_404(self, client: AsyncClient):
        """Test 404 for invalid task ID."""
        response = await client.get("/api/v1/tasks/99999")

        # Verify 404 Not Found
        assert response.status_code == 404

        # Verify error response format
        data = response.json()
        assert "detail" in data


class TestListTasks:
    """Test GET /tasks list endpoint."""

    @pytest.mark.asyncio
    async def test_list_all_tasks(self, client: AsyncClient):
        """T019: Create multiple tasks and list all."""
        # Create 3 tasks
        tasks = [
            {"title": "Task 1", "priority": "high"},
            {"title": "Task 2", "priority": "medium"},
            {"title": "Task 3", "priority": "low"},
        ]

        for task_data in tasks:
            response = await client.post("/api/v1/tasks/", json=task_data)
            assert response.status_code == 201

        # List all tasks
        response = await client.get("/api/v1/tasks/")

        # Verify 200 OK
        assert response.status_code == 200

        # Verify response structure
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data

        # Verify task count
        assert len(data["tasks"]) >= 3
        assert data["total"] >= 3


class TestFilterTasks:
    """Test GET /tasks filtering."""

    @pytest.mark.asyncio
    async def test_filter_by_status(self, client: AsyncClient):
        """T020: Filter tasks by status."""
        # Create tasks with different statuses
        await client.post("/tasks", json={"title": "Pending task", "status": "pending"})
        await client.post(
            "/tasks", json={"title": "In progress task", "status": "in_progress"}
        )
        await client.post(
            "/tasks", json={"title": "Completed task", "status": "completed"}
        )

        # Filter by status=pending
        response = await client.get("/api/v1/tasks/?status=pending")
        assert response.status_code == 200

        data = response.json()
        # All returned tasks should have status=pending
        for task in data["tasks"]:
            assert task["status"] == "pending"

    @pytest.mark.asyncio
    async def test_filter_by_priority(self, client: AsyncClient):
        """Filter tasks by priority."""
        # Create tasks with different priorities
        await client.post(
            "/tasks", json={"title": "Critical task", "priority": "critical"}
        )
        await client.post("/tasks", json={"title": "High task", "priority": "high"})
        await client.post("/tasks", json={"title": "Low task", "priority": "low"})

        # Filter by priority=critical
        response = await client.get("/api/v1/tasks/?priority=critical")
        assert response.status_code == 200

        data = response.json()
        # All returned tasks should have priority=critical
        for task in data["tasks"]:
            assert task["priority"] == "critical"

    @pytest.mark.asyncio
    async def test_filter_by_tag(self, client: AsyncClient):
        """Filter tasks by tag."""
        # Create tasks with different tags
        await client.post(
            "/tasks", json={"title": "Bug task", "tags": ["bug", "urgent"]}
        )
        await client.post("/tasks", json={"title": "Feature task", "tags": ["feature"]})
        await client.post(
            "/tasks", json={"title": "Doc task", "tags": ["documentation"]}
        )

        # Filter by tag=bug
        response = await client.get("/api/v1/tasks/?tag=bug")
        assert response.status_code == 200

        data = response.json()
        # All returned tasks should contain tag "bug"
        for task in data["tasks"]:
            assert "bug" in task["tags"]


class TestUpdateTask:
    """Test PATCH /tasks/{id} endpoint."""

    @pytest.mark.asyncio
    async def test_update_task_single_field(self, client: AsyncClient):
        """T032: Update single field with optimistic locking."""
        # Create task
        task_data = {
            "title": "Original task",
            "status": "pending",
            "priority": "medium",
        }
        create_response = await client.post("/api/v1/tasks/", json=task_data)
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]
        original_version = task["version"]

        # Update status only
        update_data = {"status": "in_progress"}
        response = await client.patch(
            f"/api/v1/tasks/{task_id}?If-Match={original_version}",
            json=update_data,
        )

        # Verify 200 OK
        assert response.status_code == 200

        # Verify update
        data = response.json()
        assert data["id"] == task_id
        assert data["status"] == "in_progress"
        assert data["title"] == task["title"]  # Unchanged
        assert data["priority"] == task["priority"]  # Unchanged
        assert data["version"] == original_version + 1  # Incremented

    @pytest.mark.asyncio
    async def test_update_task_multiple_fields(self, client: AsyncClient):
        """T033: Update multiple fields simultaneously."""
        # Create task
        task_data = {
            "title": "Original task",
            "status": "pending",
            "priority": "low",
            "tags": [],
        }
        create_response = await client.post("/api/v1/tasks/", json=task_data)
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]
        version = task["version"]

        # Update multiple fields
        update_data = {
            "title": "Updated task",
            "status": "completed",
            "priority": "high",
            "tags": ["urgent", "done"],
        }
        response = await client.patch(
            f"/api/v1/tasks/{task_id}?If-Match={version}",
            json=update_data,
        )

        # Verify 200 OK
        assert response.status_code == 200

        # Verify all updates applied
        data = response.json()
        assert data["title"] == "Updated task"
        assert data["status"] == "completed"
        assert data["priority"] == "high"
        assert data["tags"] == ["urgent", "done"]
        assert data["version"] == version + 1

    @pytest.mark.asyncio
    async def test_optimistic_locking_conflict(self, client: AsyncClient):
        """T034: Test version conflict with optimistic locking."""
        # Create task
        task_data = {"title": "Test task"}
        create_response = await client.post("/api/v1/tasks/", json=task_data)
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]
        version = task["version"]

        # First update (should succeed)
        update1 = {"status": "in_progress"}
        response1 = await client.patch(
            f"/api/v1/tasks/{task_id}?If-Match={version}",
            json=update1,
        )
        assert response1.status_code == 200
        assert response1.json()["version"] == version + 1

        # Second update with stale version (should fail with 409)
        update2 = {"status": "completed"}
        response2 = await client.patch(
            f"/api/v1/tasks/{task_id}?If-Match={version}",  # Using old version
            json=update2,
        )

        # Verify 409 Conflict
        assert response2.status_code == 409

        # Verify error response structure
        # HTTPException wraps the detail dict in a "detail" field
        response_json = response2.json()
        error_data = (
            response_json
            if "code" in response_json
            else response_json.get("detail", {})
        )
        assert error_data["code"] == "VERSION_CONFLICT"
        assert "current_version" in error_data
        assert "requested_version" in error_data
        assert error_data["current_version"] == version + 1
        assert error_data["requested_version"] == version

    @pytest.mark.asyncio
    async def test_update_nonexistent_task(self, client: AsyncClient):
        """T035: Test PATCH on non-existent task returns 404."""
        update_data = {"title": "Updated"}
        response = await client.patch(
            "/api/v1/tasks/99999?If-Match=1",
            json=update_data,
        )

        # Verify 404 Not Found
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_without_version(self, client: AsyncClient):
        """T035: Test PATCH without If-Match header (optional for this API)."""
        # Create task
        task_data = {"title": "Test task"}
        create_response = await client.post("/api/v1/tasks/", json=task_data)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Update without If-Match (should still work, version check is optional)
        update_data = {"title": "Updated without version"}
        response = await client.patch(
            f"/api/v1/tasks/{task_id}",
            json=update_data,
        )

        # Should succeed (version check is optional)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated without version"


class TestDeleteTask:
    """Test DELETE /tasks/{id} endpoint."""

    @pytest.mark.asyncio
    async def test_delete_task(self, client: AsyncClient):
        """T040: Delete task and verify 204 response."""
        # Create task
        task_data = {"title": "Task to delete"}
        create_response = await client.post("/api/v1/tasks/", json=task_data)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # Delete task
        response = await client.delete(f"/api/v1/tasks/{task_id}")

        # Verify 204 No Content
        assert response.status_code == 204
        assert response.content == b""  # Empty body

    @pytest.mark.asyncio
    async def test_delete_task_verification(self, client: AsyncClient):
        """T041: Verify deleted task cannot be retrieved."""
        # Create task
        task_data = {"title": "Task to delete and verify"}
        create_response = await client.post("/api/v1/tasks/", json=task_data)
        assert create_response.status_code == 201
        task = create_response.json()
        task_id = task["id"]

        # Delete task
        delete_response = await client.delete(f"/api/v1/tasks/{task_id}")
        assert delete_response.status_code == 204

        # Try to retrieve deleted task
        get_response = await client.get(f"/api/v1/tasks/{task_id}")
        assert get_response.status_code == 404

        # Verify task is not in list
        list_response = await client.get("/api/v1/tasks/")
        assert list_response.status_code == 200
        tasks = list_response.json()["tasks"]
        task_ids = [t["id"] for t in tasks]
        assert task_id not in task_ids

    @pytest.mark.asyncio
    async def test_delete_nonexistent_task(self, client: AsyncClient):
        """T042: Delete non-existent task returns 404."""
        response = await client.delete("/api/v1/tasks/99999")

        # Verify 404 Not Found
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_idempotent(self, client: AsyncClient):
        """T042: Deleting same task twice is idempotent."""
        # Create task
        task_data = {"title": "Task for idempotent delete"}
        create_response = await client.post("/api/v1/tasks/", json=task_data)
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # First delete (should succeed)
        response1 = await client.delete(f"/api/v1/tasks/{task_id}")
        assert response1.status_code == 204

        # Second delete (should return 404 - not found)
        response2 = await client.delete(f"/api/v1/tasks/{task_id}")
        assert response2.status_code == 404
