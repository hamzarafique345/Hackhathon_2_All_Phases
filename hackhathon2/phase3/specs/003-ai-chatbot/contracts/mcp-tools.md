# MCP Tool Definitions: Task Management Tools

**Feature**: 003-ai-chatbot
**Date**: 2026-01-24
**Protocol**: Model Context Protocol (MCP)

## Overview

This document defines the MCP tools available to the OpenSDK AI agent for task management operations. Each tool maps one-to-one to a Phase 2 REST API endpoint, maintaining strict isolation between the AI agent and the database.

---

## Tool Definitions

### 1. list_tasks

**Description**: Retrieve all tasks for the authenticated user, optionally filtered by completion status.

**Purpose**: Allows AI to show user their tasks in response to queries like "What are my tasks?" or "Show me incomplete tasks"

**Parameters**:
```yaml
name: list_tasks
description: List all tasks for the authenticated user
parameters:
  type: object
  properties:
    completed:
      type: boolean
      description: Filter by completion status (optional)
      required: false
  required: []
```

**Implementation**:
- Extracts `user_id` from JWT token (not from parameters)
- Calls: `GET /api/{user_id}/tasks`
- Query params: `?completed={true|false}` if filter provided
- Returns: Array of task objects

**Response Format**:
```json
{
  "success": true,
  "tasks": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-24T10:00:00Z"
    }
  ],
  "count": 1
}
```

**Error Handling**:
- 401 Unauthorized: Return error message to AI
- 403 Forbidden: Return error message to AI
- 500 Server Error: Return error message to AI

---

### 2. create_task

**Description**: Create a new task with the specified title and optional description.

**Purpose**: Allows AI to create tasks in response to user requests like "Add a task to buy groceries"

**Parameters**:
```yaml
name: create_task
description: Create a new task for the authenticated user
parameters:
  type: object
  properties:
    title:
      type: string
      description: Task title (required)
      minLength: 1
      maxLength: 255
    description:
      type: string
      description: Task description (optional)
      maxLength: 10000
  required:
    - title
```

**Implementation**:
- Extracts `user_id` from JWT token
- Validates `title` is non-empty
- Calls: `POST /api/{user_id}/tasks`
- Body: `{ "title": "...", "description": "..." }`
- Returns: Created task object

**Response Format**:
```json
{
  "success": true,
  "task": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-24T10:00:00Z"
  }
}
```

**Error Handling**:
- 400 Bad Request: Return validation error to AI
- 401 Unauthorized: Return error message to AI
- 403 Forbidden: Return error message to AI

---

### 3. get_task

**Description**: Retrieve details of a specific task by ID.

**Purpose**: Allows AI to get task details when user references a specific task

**Parameters**:
```yaml
name: get_task
description: Get details of a specific task
parameters:
  type: object
  properties:
    task_id:
      type: string
      format: uuid
      description: Task ID to retrieve
  required:
    - task_id
```

**Implementation**:
- Extracts `user_id` from JWT token
- Validates `task_id` is valid UUID
- Calls: `GET /api/{user_id}/tasks/{task_id}`
- Returns: Task object

**Response Format**:
```json
{
  "success": true,
  "task": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-24T10:00:00Z"
  }
}
```

**Error Handling**:
- 404 Not Found: Return "Task not found" to AI
- 403 Forbidden: Return "Cannot access this task" to AI

---

### 4. update_task

**Description**: Update a task's title and/or description.

**Purpose**: Allows AI to modify task details in response to user requests like "Change the grocery task to include eggs"

**Parameters**:
```yaml
name: update_task
description: Update a task's title and/or description
parameters:
  type: object
  properties:
    task_id:
      type: string
      format: uuid
      description: Task ID to update
    title:
      type: string
      description: New task title (optional)
      minLength: 1
      maxLength: 255
    description:
      type: string
      description: New task description (optional)
      maxLength: 10000
  required:
    - task_id
```

**Implementation**:
- Extracts `user_id` from JWT token
- Validates `task_id` is valid UUID
- At least one of `title` or `description` must be provided
- Calls: `PUT /api/{user_id}/tasks/{task_id}`
- Body: `{ "title": "...", "description": "...", "completed": <current_value> }`
- Note: Must include current `completed` status (fetch first if needed)
- Returns: Updated task object

**Response Format**:
```json
{
  "success": true,
  "task": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "Buy groceries and eggs",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-24T10:00:00Z"
  }
}
```

**Error Handling**:
- 400 Bad Request: Return validation error to AI
- 404 Not Found: Return "Task not found" to AI
- 403 Forbidden: Return "Cannot update this task" to AI

---

### 5. complete_task

**Description**: Toggle a task's completion status (mark as complete or incomplete).

**Purpose**: Allows AI to mark tasks complete/incomplete in response to user requests like "Mark the grocery task as done"

**Parameters**:
```yaml
name: complete_task
description: Toggle task completion status
parameters:
  type: object
  properties:
    task_id:
      type: string
      format: uuid
      description: Task ID to toggle
    completed:
      type: boolean
      description: New completion status (true = complete, false = incomplete)
  required:
    - task_id
    - completed
```

**Implementation**:
- Extracts `user_id` from JWT token
- Validates `task_id` is valid UUID
- Calls: `PATCH /api/{user_id}/tasks/{task_id}/complete`
- Body: `{ "completed": true/false }`
- Returns: Updated task object

**Response Format**:
```json
{
  "success": true,
  "task": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": true,
    "created_at": "2026-01-24T10:00:00Z"
  }
}
```

**Error Handling**:
- 404 Not Found: Return "Task not found" to AI
- 403 Forbidden: Return "Cannot modify this task" to AI

---

### 6. delete_task

**Description**: Delete a task permanently.

**Purpose**: Allows AI to delete tasks in response to user requests like "Delete the grocery task" (after confirmation)

**Parameters**:
```yaml
name: delete_task
description: Delete a task permanently
parameters:
  type: object
  properties:
    task_id:
      type: string
      format: uuid
      description: Task ID to delete
  required:
    - task_id
```

**Implementation**:
- Extracts `user_id` from JWT token
- Validates `task_id` is valid UUID
- Calls: `DELETE /api/{user_id}/tasks/{task_id}`
- Returns: Success confirmation

**Response Format**:
```json
{
  "success": true,
  "message": "Task deleted successfully",
  "task_id": "uuid"
}
```

**Error Handling**:
- 404 Not Found: Return "Task not found" to AI
- 403 Forbidden: Return "Cannot delete this task" to AI

---

## Tool Implementation Pattern

### Python Implementation Template

```python
import httpx
import jwt
import os
from typing import Dict, Any, Optional

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

def extract_user_id_from_jwt(token: str) -> str:
    """Extract user_id from JWT token"""
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid JWT token: {e}")

def list_tasks(jwt_token: str, completed: Optional[bool] = None) -> Dict[str, Any]:
    """MCP tool: List tasks"""
    try:
        user_id = extract_user_id_from_jwt(jwt_token)

        url = f"{API_BASE_URL}/api/{user_id}/tasks"
        params = {}
        if completed is not None:
            params["completed"] = completed

        response = httpx.get(
            url,
            headers={"Authorization": f"Bearer {jwt_token}"},
            params=params,
            timeout=10.0
        )

        if response.status_code == 200:
            tasks = response.json()
            return {
                "success": True,
                "tasks": tasks,
                "count": len(tasks)
            }
        else:
            return {
                "success": False,
                "error": response.json().get("detail", "Failed to list tasks")
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error listing tasks: {str(e)}"
        }

def create_task(jwt_token: str, title: str, description: str = "") -> Dict[str, Any]:
    """MCP tool: Create task"""
    try:
        user_id = extract_user_id_from_jwt(jwt_token)

        if not title or not title.strip():
            return {
                "success": False,
                "error": "Task title cannot be empty"
            }

        response = httpx.post(
            f"{API_BASE_URL}/api/{user_id}/tasks",
            headers={"Authorization": f"Bearer {jwt_token}"},
            json={"title": title.strip(), "description": description.strip()},
            timeout=10.0
        )

        if response.status_code == 201:
            return {
                "success": True,
                "task": response.json()
            }
        else:
            return {
                "success": False,
                "error": response.json().get("detail", "Failed to create task")
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error creating task: {str(e)}"
        }

# Similar implementations for get_task, update_task, complete_task, delete_task...
```

---

## Tool Registration with OpenSDK

```python
from opensdk import Agent, Tool

# Define tools
tools = [
    Tool(
        name="list_tasks",
        description="List all tasks for the authenticated user",
        function=list_tasks,
        parameters={
            "type": "object",
            "properties": {
                "completed": {
                    "type": "boolean",
                    "description": "Filter by completion status (optional)"
                }
            }
        }
    ),
    Tool(
        name="create_task",
        description="Create a new task",
        function=create_task,
        parameters={
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Task title"},
                "description": {"type": "string", "description": "Task description"}
            },
            "required": ["title"]
        }
    ),
    # ... register other tools
]

# Initialize agent with tools
agent = Agent(
    model="meta-llama/llama-3.2-3b-instruct:free",
    provider="openrouter",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    tools=tools
)
```

---

## Security Considerations

### JWT Token Handling

1. **Token Extraction**: Tools MUST extract `user_id` from JWT token, not accept as parameter
2. **Token Validation**: Phase 2 APIs validate token independently (defense in depth)
3. **Token Propagation**: JWT token passed from conversation API → AI agent → MCP tools → Phase 2 APIs
4. **Token Expiration**: Tools handle 401 errors gracefully, return error to AI

### Authorization

1. **User Isolation**: `user_id` from JWT ensures users only access their own tasks
2. **No Bypass**: AI cannot bypass authorization by providing different `user_id`
3. **API Validation**: Phase 2 APIs validate `user_id` in URL matches JWT claim

### Input Validation

1. **Parameter Validation**: Tools validate inputs before API calls
2. **Sanitization**: Trim whitespace, check lengths, validate UUIDs
3. **Error Handling**: Return structured errors to AI, not raw exceptions

---

## Testing MCP Tools

### Unit Tests

```python
import pytest
from unittest.mock import patch, Mock

def test_list_tasks_success():
    """Test list_tasks with successful API response"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"id": "uuid1", "title": "Task 1", "completed": False}
    ]

    with patch("httpx.get", return_value=mock_response):
        result = list_tasks("valid_jwt_token")

    assert result["success"] is True
    assert len(result["tasks"]) == 1
    assert result["count"] == 1

def test_create_task_empty_title():
    """Test create_task with empty title"""
    result = create_task("valid_jwt_token", title="")

    assert result["success"] is False
    assert "empty" in result["error"].lower()

# ... more tests
```

### Integration Tests

```python
def test_create_and_list_tasks_integration():
    """Test creating a task and then listing it"""
    # Create task
    create_result = create_task(
        jwt_token=test_jwt_token,
        title="Integration Test Task",
        description="Test description"
    )
    assert create_result["success"] is True
    task_id = create_result["task"]["id"]

    # List tasks
    list_result = list_tasks(jwt_token=test_jwt_token)
    assert list_result["success"] is True
    assert any(task["id"] == task_id for task in list_result["tasks"])
```

---

**MCP Tools Status**: ✅ Complete
**Next Phase**: Quickstart Documentation
