"""
JWT authentication utilities and FastAPI dependencies.
"""
import os
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable is not set")

# HTTP Bearer token scheme
security = HTTPBearer()


def create_jwt_token(user_id: UUID, email: str, remember_me: bool = False) -> str:
    """
    Create a JWT token for authenticated user.

    Args:
        user_id: User's unique identifier
        email: User's email address
        remember_me: If True, token expires in 7 days; otherwise session-based (24 hours)

    Returns:
        Encoded JWT token string
    """
    expiration = timedelta(days=7) if remember_me else timedelta(hours=24)
    expire = datetime.utcnow() + expiration

    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow()
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_jwt_token(token: str) -> dict:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    FastAPI dependency to get current authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer token from Authorization header

    Returns:
        User payload from decoded JWT token

    Raises:
        HTTPException: If token is missing or invalid
    """
    token = credentials.credentials
    payload = verify_jwt_token(token)
    return payload
