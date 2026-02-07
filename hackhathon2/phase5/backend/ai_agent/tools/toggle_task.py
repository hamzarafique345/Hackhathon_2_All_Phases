"""
MCP tool for toggling task completion status via Phase 2 API.
"""
import os
import httpx
from typing import Dict, Any
from . import extract_user_id_from_jwt, format_tool_response


async def toggle_task(jwt_token: str, task_id: str) -> Dict[str, Any]:
    """
    Toggle the completion status of a task.

    Args:
        jwt_token: JWT authentication token
        task_id: Task ID to toggle

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

        # Build request URL
        url = f"{api_base}/api/users/{user_id}/tasks/{task_id}/toggle"

        # Make HTTP request to Phase 2 API
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.patch(
                url,
                headers={"Authorization": f"Bearer {jwt_token}"},
            )

        # Handle response
        if response.status_code == 200:
            task = response.json()
            status = "completed" if task.get("completed") else "incomplete"
            return format_tool_response(
                success=True,
                data={"task": task, "status": status}
            )
        elif response.status_code == 404:
            return format_tool_response(
                success=False,
                error="Task not found"
            )
        else:
            error_detail = response.json().get("detail", "Failed to toggle task")
            return format_tool_response(success=False, error=error_detail)

    except ValueError as e:
        return format_tool_response(success=False, error=str(e))
    except Exception as e:
        return format_tool_response(
            success=False,
            error=f"Error toggling task: {str(e)}"
        )
