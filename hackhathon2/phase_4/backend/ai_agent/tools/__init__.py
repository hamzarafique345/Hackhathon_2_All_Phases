"""
Utility functions for MCP tools.
"""
import os
import jwt
from typing import Dict, Any


def extract_user_id_from_jwt(token: str) -> str:
    """
    Extract user_id from JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID as string

    Raises:
        ValueError: If token is invalid or user_id not found
    """
    try:
        # Get secret from environment
        secret = os.getenv("BETTER_AUTH_SECRET")
        if not secret:
            raise ValueError("BETTER_AUTH_SECRET not configured")

        # Decode JWT token
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"]
        )

        # Extract user_id
        user_id = payload.get("user_id") or payload.get("sub")
        if not user_id:
            raise ValueError("user_id not found in JWT token")

        return str(user_id)

    except jwt.ExpiredSignatureError:
        raise ValueError("JWT token has expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid JWT token: {str(e)}")


def format_tool_response(success: bool, data: Any = None, error: str = None) -> Dict[str, Any]:
    """
    Format a standardized tool response.

    Args:
        success: Whether the operation succeeded
        data: Response data (if successful)
        error: Error message (if failed)

    Returns:
        Formatted response dictionary
    """
    response = {"success": success}

    if success and data is not None:
        response["data"] = data

    if not success and error:
        response["error"] = error

    return response
