"""
FastAPI main application with authentication endpoints.
"""
import os
from datetime import datetime
from typing import Optional
from uuid import UUID
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dotenv import load_dotenv

from src.database import create_db_and_tables, get_session
from src.models import User, Task
from src.auth import create_jwt_token, get_current_user
from typing import List

# Phase 3: Import conversation API router
from src.api.conversations import router as conversation_router

# Load environment variables
load_dotenv()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create FastAPI app
app = FastAPI(
    title="Todo App API",
    description="Authentication and task management API",
    version="1.0.0"
)

# CORS configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Phase 3: Register conversation API router
app.include_router(conversation_router)


# Pydantic models for request/response
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None


class SignInRequest(BaseModel):
    email: EmailStr
    password: str
    rememberMe: Optional[bool] = False


class UserResponse(BaseModel):
    id: UUID
    email: str
    name: Optional[str]
    created_at: datetime


class AuthResponse(BaseModel):
    user: UserResponse
    token: str
    expiresAt: datetime


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    database: str


# Task management models
class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool


class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime


# Startup event to create tables
@app.on_event("startup")
async def on_startup():
    """Create database tables on application startup."""
    await create_db_and_tables()


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint with API information and documentation links.
    """
    return {
        "message": "Todo App API",
        "version": "1.0.0",
        "status": "running",
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "health": "/health",
            "auth": {
                "signup": "/auth/signup",
                "signin": "/auth/signin",
                "verify": "/auth/verify"
            },
            "tasks": "/api/users/{user_id}/tasks"
        }
    }


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify service availability.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        database="connected"
    )


# Sign-up endpoint
@app.post("/auth/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignUpRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Register a new user account.

    - Validates email format and password length
    - Checks for duplicate email addresses
    - Hashes password with bcrypt (12 rounds minimum)
    - Issues JWT token upon successful registration
    """
    # Validate password length
    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )

    # Bcrypt has a 72-byte limit, validate password length
    if len(request.password.encode('utf-8')) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too long (maximum 72 bytes)"
        )

    # Check if email already exists
    result = await session.execute(
        select(User).where(User.email == request.email.lower())
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Hash password
    password_hash = pwd_context.hash(request.password)

    # Create new user
    new_user = User(
        email=request.email.lower(),
        password_hash=password_hash,
        name=request.name
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    # Generate JWT token
    token = create_jwt_token(new_user.id, new_user.email, remember_me=False)

    # Calculate expiration time (24 hours for new signups)
    from datetime import timedelta
    expires_at = datetime.utcnow() + timedelta(hours=24)

    return AuthResponse(
        user=UserResponse(
            id=new_user.id,
            email=new_user.email,
            name=new_user.name,
            created_at=new_user.created_at
        ),
        token=token,
        expiresAt=expires_at
    )


# Sign-in endpoint
@app.post("/auth/signin", response_model=AuthResponse)
async def signin(
    request: SignInRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Authenticate user with email and password.

    - Verifies credentials against stored user accounts
    - Issues JWT token upon successful authentication
    - Supports "Remember me" for 7-day sessions
    """
    # Find user by email
    result = await session.execute(
        select(User).where(User.email == request.email.lower())
    )
    user = result.scalar_one_or_none()

    # Verify user exists and password is correct
    if not user or not pwd_context.verify(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    token = create_jwt_token(user.id, user.email, remember_me=request.rememberMe)

    # Calculate expiration time
    from datetime import timedelta
    expiration = timedelta(days=7) if request.rememberMe else timedelta(hours=24)
    expires_at = datetime.utcnow() + expiration

    return AuthResponse(
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at
        ),
        token=token,
        expiresAt=expires_at
    )


# Verify token endpoint
@app.get("/auth/verify", response_model=UserResponse)
async def verify_token(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Verify JWT token validity and return user information.

    - Validates JWT token from Authorization header
    - Returns user details if token is valid
    """
    # Get user from database
    user_id = UUID(current_user["sub"])
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at
    )


# Task Management Endpoints

# Get all tasks for a user
@app.get("/api/users/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(
    user_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Fetch all tasks for the authenticated user.

    - Requires valid JWT token
    - Users can only access their own tasks
    - Returns tasks ordered by creation date (newest first)
    """
    # Verify user_id matches JWT claim
    if str(user_id) != current_user["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    # Query tasks for user
    result = await session.execute(
        select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    )
    tasks = result.scalars().all()

    return tasks


# Create a new task
@app.post("/api/users/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: UUID,
    request: TaskCreateRequest,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    - Requires valid JWT token
    - Title is required (max 255 characters)
    - Description is optional
    """
    # Verify authorization
    if str(user_id) != current_user["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Validate title
    if not request.title or not request.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required"
        )

    if len(request.title) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must be 255 characters or less"
        )

    # Create task
    new_task = Task(
        user_id=user_id,
        title=request.title.strip(),
        description=request.description.strip() if request.description else None
    )

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    return new_task


# Update a task
@app.put("/api/users/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: UUID,
    task_id: UUID,
    request: TaskUpdateRequest,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update an existing task.

    - Requires valid JWT token
    - Users can only update their own tasks
    - Updates title, description, and completion status
    """
    # Verify authorization
    if str(user_id) != current_user["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update tasks for this user"
        )

    # Find task
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Validate title
    if not request.title or not request.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required"
        )

    if len(request.title) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must be 255 characters or less"
        )

    # Update task
    task.title = request.title.strip()
    task.description = request.description.strip() if request.description else None
    task.completed = request.completed

    await session.commit()
    await session.refresh(task)

    return task


# Toggle task completion status
@app.patch("/api/users/{user_id}/tasks/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task(
    user_id: UUID,
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Toggle the completion status of a task.

    - Requires valid JWT token
    - Users can only toggle their own tasks
    - Flips completed status (true -> false, false -> true)
    """
    # Verify authorization
    if str(user_id) != current_user["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update tasks for this user"
        )

    # Find task
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion
    task.completed = not task.completed

    await session.commit()
    await session.refresh(task)

    return task


# Delete a task
@app.delete("/api/users/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: UUID,
    task_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a task.

    - Requires valid JWT token
    - Users can only delete their own tasks
    - Returns 204 No Content on success
    """
    # Verify authorization
    if str(user_id) != current_user["sub"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete tasks for this user"
        )

    # Find task
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete task
    await session.delete(task)
    await session.commit()

    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
