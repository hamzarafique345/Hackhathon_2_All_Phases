# JWT Token Fix for AI Agent Task Creation

## Issue
When asking the chatbot to create a task, it failed with:
```
I couldn't create the task. Error: Invalid JWT token: Not enough segments
```

## Root Cause

The AI agent was receiving an **empty string** (`""`) as the JWT token instead of the actual token from the Authorization header.

### Code Analysis

**Location**: `backend/src/api/conversations.py` (lines 178-180)

**Before (Broken)**:
```python
# Get JWT token from request (simplified - in production, extract from Authorization header)
# For now, we'll use a placeholder since we need the actual token
jwt_token = getattr(current_user, "_jwt_token", "")
```

**Problem**:
- `current_user` is a dictionary (JWT payload), not an object
- It doesn't have a `_jwt_token` attribute
- `getattr()` always returned the default value: `""`
- Empty string was passed to AI agent → "Not enough segments" error

**After (Fixed)**:
```python
# Get JWT token from Authorization header
jwt_token = credentials.credentials
```

**Solution**:
- Added `credentials: HTTPAuthorizationCredentials = Depends(security)` parameter
- Extract actual JWT token from Authorization header
- Pass valid token to AI agent

## Changes Made

### 1. Import Statement (Line 5)
```python
# Added HTTPAuthorizationCredentials import
from fastapi.security import HTTPAuthorizationCredentials
```

### 2. Import Statement (Line 18)
```python
# Added security import
from ..auth import get_current_user, security
```

### 3. Function Signature (Line 140)
```python
# Added credentials parameter
async def create_message(
    user_id: UUID,
    conversation_id: UUID,
    data: MessageCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),  # NEW
):
```

### 4. Token Extraction (Line 179)
```python
# Extract actual token from credentials
jwt_token = credentials.credentials
```

## How It Works

### Request Flow:
1. **Frontend** sends message with `Authorization: Bearer <token>` header
2. **FastAPI** extracts token via `security` dependency
3. **credentials.credentials** contains the actual JWT token string
4. **AI Agent** receives valid token
5. **AI Agent Tools** (create_task, list_tasks) use token to authenticate API calls

### Token Validation:
```python
# In ai_agent/tools/__init__.py
def extract_user_id_from_jwt(token: str) -> str:
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    user_id = payload.get("user_id") or payload.get("sub")
    return str(user_id)
```

## Testing

### Valid Token Test:
```python
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
payload = jwt.decode(token, secret, algorithms=['HS256'])
# Result: {'sub': 'e31c4649-...', 'email': 'hamza123@gmail.com', ...}
```

### Empty Token Test (The Bug):
```python
token = ""
jwt.decode(token, secret, algorithms=['HS256'])
# Error: DecodeError - Not enough segments
```

## Verification

After the fix, the AI agent can now:
- ✅ Receive valid JWT token
- ✅ Extract user_id from token
- ✅ Make authenticated API calls to create/list tasks
- ✅ Return success responses to the user

## Related Files

- `backend/src/api/conversations.py` - Main fix location
- `backend/src/auth.py` - JWT verification and security dependency
- `backend/ai_agent/tools/__init__.py` - Token extraction utility
- `backend/ai_agent/tools/create_task.py` - Task creation tool
- `backend/ai_agent/tools/list_tasks.py` - Task listing tool

## Complete Fix Summary

This is the **second major fix** for the chatbot:

1. **First Fix**: Database schema and `current_user.id` → `current_user["sub"]`
2. **Second Fix**: JWT token passing to AI agent (this document)

Both fixes are now applied and the chatbot should work end-to-end!
