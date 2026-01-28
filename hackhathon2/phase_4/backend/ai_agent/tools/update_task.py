"""
MCP tool for updating tasks via Phase 2 API.
"""
import os
import httpx
from typing import Dict, Any, Optional
from . import extract_user_id_from_jwt, format_tool_response


async def update_task(
    jwt_token: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Update an existing task.

    Args:
        jwt_token: JWT authentication token
        task_id: Task ID to update
        title: New task title (optional)
        description: New task description (optional)
        completed: New completion status (optional)

    Returns:
        Formatted response with updated task or error
    """
    try:
        # Validate input
        if not task_id or not task_id.strip():
            return format_tool_response(
                success=False,
                error="Task ID cannot be empty"
            )

        # Extract user_id from JWT token
        user_id = extract_user_id_from_jwt(jwt_token)

        # Get API base URL
        api_base = os.getenv("API_BASE_URL", "http://localhost:8000")

        # First, get the current task to preserve unchanged fields
        get_url = f"{api_base}/api/users/{user_id}/tasks"
        async with httpx.AsyncClient(timeout=10.0) as client:
            get_response = await client.get(
                get_url,
                headers={"Authorization": f"Bearer {jwt_token}"},
            )

        if get_response.status_code != 200:
            return format_tool_response(
                success=False,
                error="Failed to retrieve current task data"
            )

        # Find the task in the list
        tasks = get_response.json()
        current_task = None
        for task in tasks:
            if task.get("id") == task_id:
                current_task = task
                break

        if not current_task:
            return format_tool_response(
                success=False,
                error="Task not found"
            )

        # Build request URL for update
        url = f"{api_base}/api/users/{user_id}/tasks/{task_id}"

        # Prepare request body with current values as defaults
        body = {
            "title": title.strip() if title else current_task.get("title"),
            "description": description.strip() if description else current_task.get("description", ""),
            "completed": completed if completed is not None else current_task.get("completed", False),
        }

        # Validate title
        if not body["title"] or not body["title"].strip():
            return format_tool_response(
                success=False,
                error="Task title cannot be empty"
            )

        # Make HTTP request to Phase 2 API
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.put(
                url,
                headers={"Authorization": f"Bearer {jwt_token}"},
                json=body,
            )

        # Handle response
        if response.status_code == 200:
            task = response.json()
            return format_tool_response(success=True, data={"task": task})
        elif response.status_code == 404:
            return format_tool_response(
                success=False,
                error="Task not found"
            )
        else:
            error_detail = response.json().get("detail", "Failed to update task")
            return format_tool_response(success=False, error=error_detail)

    except ValueError as e:
        return format_tool_response(success=False, error=str(e))
    except Exception as e:
        return format_tool_response(
            success=False,
            error=f"Error updating task: {str(e)}"
        )
