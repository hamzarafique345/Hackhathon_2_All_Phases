"""
MCP tool for deleting tasks via Phase 2 API.
"""
import os
import httpx
from typing import Dict, Any
from . import extract_user_id_from_jwt, format_tool_response


async def delete_task(jwt_token: str, task_id: str) -> Dict[str, Any]:
    """
    Delete a task.

    Args:
        jwt_token: JWT authentication token
        task_id: Task ID to delete

    Returns:
        Formatted response with success status or error
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
        url = f"{api_base}/api/users/{user_id}/tasks/{task_id}"

        # Make HTTP request to Phase 2 API
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.delete(
                url,
                headers={"Authorization": f"Bearer {jwt_token}"},
            )

        # Handle response
        if response.status_code == 204:
            return format_tool_response(
                success=True,
                data={"message": "Task deleted successfully"}
            )
        elif response.status_code == 404:
            return format_tool_response(
                success=False,
                error="Task not found"
            )
        else:
            error_detail = response.json().get("detail", "Failed to delete task")
            return format_tool_response(success=False, error=error_detail)

    except ValueError as e:
        return format_tool_response(success=False, error=str(e))
    except Exception as e:
        return format_tool_response(
            success=False,
            error=f"Error deleting task: {str(e)}"
        )
