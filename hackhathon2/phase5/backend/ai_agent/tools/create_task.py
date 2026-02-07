"""
MCP tool for creating tasks via Phase 2 API.
"""
import os
import httpx
from typing import Dict, Any
from . import extract_user_id_from_jwt, format_tool_response


async def create_task(jwt_token: str, title: str, description: str = "") -> Dict[str, Any]:
    """
    Create a new task for the authenticated user.

    Args:
        jwt_token: JWT authentication token
        title: Task title (required)
        description: Task description (optional)

    Returns:
        Formatted response with created task or error
    """
    try:
        # Validate input
        if not title or not title.strip():
            return format_tool_response(
                success=False,
                error="Task title cannot be empty"
            )

        # Extract user_id from JWT token
        user_id = extract_user_id_from_jwt(jwt_token)

        # Get API base URL
        api_base = os.getenv("API_BASE_URL", "http://localhost:8000")

        # Build request URL
        url = f"{api_base}/api/users/{user_id}/tasks"

        # Prepare request body
        body = {
            "title": title.strip(),
            "description": description.strip() if description else None,
        }

        # Make HTTP request to Phase 2 API
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {jwt_token}"},
                json=body,
            )

        # Handle response
        if response.status_code == 201:
            task = response.json()
            return format_tool_response(success=True, data={"task": task})
        else:
            error_detail = response.json().get("detail", "Failed to create task")
            return format_tool_response(success=False, error=error_detail)

    except ValueError as e:
        return format_tool_response(success=False, error=str(e))
    except Exception as e:
        return format_tool_response(
            success=False,
            error=f"Error creating task: {str(e)}"
        )
