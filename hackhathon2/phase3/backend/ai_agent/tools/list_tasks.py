"""
MCP tool for listing tasks via Phase 2 API.
"""
import os
import httpx
from typing import Dict, Any, Optional
from . import extract_user_id_from_jwt, format_tool_response


async def list_tasks(
    jwt_token: str,
    completed: Optional[bool] = None,
    keyword: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all tasks for the authenticated user.

    Args:
        jwt_token: JWT authentication token
        completed: Optional filter by completion status
        keyword: Optional keyword to search in task titles and descriptions

    Returns:
        Formatted response with task list or error
    """
    try:
        # Extract user_id from JWT token
        user_id = extract_user_id_from_jwt(jwt_token)

        # Get API base URL
        api_base = os.getenv("API_BASE_URL", "http://localhost:8000")

        # Build request URL
        url = f"{api_base}/api/users/{user_id}/tasks"
        params = {}
        if completed is not None:
            params["completed"] = str(completed).lower()

        # Make HTTP request to Phase 2 API
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {jwt_token}"},
                params=params,
            )

        # Handle response
        if response.status_code == 200:
            tasks = response.json()

            # Apply keyword filter if provided (client-side filtering)
            if keyword:
                keyword_lower = keyword.lower()
                tasks = [
                    task for task in tasks
                    if keyword_lower in task.get("title", "").lower()
                    or keyword_lower in task.get("description", "").lower()
                ]

            return format_tool_response(
                success=True,
                data={
                    "tasks": tasks,
                    "count": len(tasks),
                }
            )
        else:
            error_detail = response.json().get("detail", "Failed to list tasks")
            return format_tool_response(success=False, error=error_detail)

    except ValueError as e:
        return format_tool_response(success=False, error=str(e))
    except Exception as e:
        return format_tool_response(
            success=False,
            error=f"Error listing tasks: {str(e)}"
        )

