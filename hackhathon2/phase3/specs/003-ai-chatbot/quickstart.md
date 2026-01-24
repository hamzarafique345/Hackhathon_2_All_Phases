# Quickstart Guide: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2026-01-24
**Branch**: 003-ai-chatbot

## Overview

This guide provides setup instructions for developing and running the Phase 3 AI-powered Todo Chatbot feature. Phase 3 extends the existing Phase 2 Todo application with conversational AI capabilities.

---

## Prerequisites

### Phase 2 Requirements (Existing)

- **Node.js**: v18+ (for Next.js frontend)
- **Python**: 3.11+ (for FastAPI backend)
- **PostgreSQL**: Neon PostgreSQL database (cloud-hosted)
- **Git**: Version control

### Phase 3 Additional Requirements

- **OpenRouter API Key**: Free-tier account at [openrouter.ai](https://openrouter.ai)
- **OpenSDK**: Python package for AI agent orchestration
- **httpx**: Python HTTP client for MCP tools

---

## Environment Setup

### 1. Clone Repository and Checkout Branch

```bash
git clone <repository-url>
cd <repository-name>
git checkout 003-ai-chatbot
```

### 2. Backend Setup

#### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**New Phase 3 Dependencies** (add to `requirements.txt`):
```
opensdk>=1.0.0
httpx>=0.24.0
pyjwt>=2.8.0
```

#### Configure Environment Variables

Create or update `backend/.env`:

```env
# Phase 2 Variables (Existing)
DATABASE_URL=postgresql://user:password@host/database
BETTER_AUTH_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256

# Phase 3 Variables (New)
OPENROUTER_API_KEY=your-openrouter-api-key-here
API_BASE_URL=http://localhost:8000
```

**Getting OpenRouter API Key**:
1. Sign up at [openrouter.ai](https://openrouter.ai)
2. Navigate to API Keys section
3. Create new API key
4. Copy key to `.env` file

#### Run Database Migrations

```bash
# Apply Phase 3 migrations (conversations, messages tables)
alembic upgrade head
```

#### Start Backend Server

```bash
uvicorn src.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

---

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
```

**New Phase 3 Dependencies** (add to `package.json`):
```json
{
  "dependencies": {
    "@radix-ui/react-dialog": "^1.0.5",
    "date-fns": "^2.30.0"
  }
}
```

#### Configure Environment Variables

Create or update `frontend/.env.local`:

```env
# Phase 2 Variables (Existing)
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000

# Phase 3 Variables (No new frontend env vars needed)
```

#### Start Frontend Development Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

---

## Development Workflow

### 1. Verify Phase 2 Functionality

Before developing Phase 3 features, ensure Phase 2 works:

1. Navigate to `http://localhost:3000`
2. Register a new user or log in
3. Create, view, update, complete, and delete tasks
4. Verify all Phase 2 features work correctly

**Phase 2 Must Work**: Phase 3 depends on Phase 2 APIs being functional.

---

### 2. Test Database Schema

Verify Phase 3 tables were created:

```sql
-- Connect to database
psql $DATABASE_URL

-- Check conversations table
\d conversations

-- Check messages table
\d messages

-- Verify foreign keys
SELECT * FROM information_schema.table_constraints
WHERE table_name IN ('conversations', 'messages');
```

Expected output:
- `conversations` table with columns: id, user_id, title, created_at, updated_at
- `messages` table with columns: id, conversation_id, role, content, created_at
- Foreign keys: conversations.user_id → users.id, messages.conversation_id → conversations.id

---

### 3. Test Conversation API Endpoints

Use curl or Postman to test Phase 3 endpoints:

#### Get JWT Token (Phase 2)

```bash
# Login to get JWT token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Extract token from response
export JWT_TOKEN="<token-from-response>"
export USER_ID="<user-id-from-token>"
```

#### Create Conversation

```bash
curl -X POST http://localhost:8000/api/$USER_ID/conversations \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Conversation"}'

# Save conversation_id from response
export CONVERSATION_ID="<conversation-id-from-response>"
```

#### Add Message (Triggers AI)

```bash
curl -X POST http://localhost:8000/api/$USER_ID/conversations/$CONVERSATION_ID/messages \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role": "user", "content": "Create a task to buy groceries"}'
```

Expected: AI response message created, task created via MCP tool

#### List Messages

```bash
curl -X GET http://localhost:8000/api/$USER_ID/conversations/$CONVERSATION_ID/messages \
  -H "Authorization: Bearer $JWT_TOKEN"
```

Expected: Array of messages (user message + AI response)

---

### 4. Test MCP Tools

Test MCP tools independently:

```python
# backend/test_mcp_tools.py
from ai_agent.tools.list_tasks import list_tasks
from ai_agent.tools.create_task import create_task
import os

# Set JWT token from login
jwt_token = "your-jwt-token-here"

# Test list_tasks
result = list_tasks(jwt_token)
print("List tasks:", result)

# Test create_task
result = create_task(jwt_token, title="Test Task", description="Test description")
print("Create task:", result)
```

Run test:
```bash
cd backend
python test_mcp_tools.py
```

---

### 5. Test AI Agent

Test OpenSDK agent with OpenRouter:

```python
# backend/test_ai_agent.py
from ai_agent.agent import create_agent
import os

# Initialize agent
agent = create_agent()

# Test conversation
response = agent.chat(
    message="Create a task to buy groceries",
    jwt_token="your-jwt-token-here",
    conversation_history=[]
)

print("AI Response:", response)
```

Run test:
```bash
cd backend
python test_ai_agent.py
```

Expected: AI generates response, calls create_task tool, returns confirmation

---

### 6. Test Frontend Chat Interface

1. Navigate to `http://localhost:3000/dashboard`
2. Click chat button (bottom-right or header)
3. Chat interface opens (modal or slide-in panel)
4. Type message: "Create a task to buy groceries"
5. Verify:
   - Message appears in chat
   - AI response appears
   - Task appears in Phase 2 task list
6. Close chat interface
7. Verify Phase 2 task list still works

---

## Common Issues & Troubleshooting

### Issue: OpenRouter API Key Invalid

**Symptoms**: 401 errors when AI agent tries to call OpenRouter

**Solution**:
1. Verify API key in `.env` is correct
2. Check OpenRouter account is active
3. Verify free-tier model is available: `meta-llama/llama-3.2-3b-instruct:free`

### Issue: JWT Token Expired

**Symptoms**: 401 errors from conversation API

**Solution**:
1. Re-login to get new JWT token
2. Check `BETTER_AUTH_SECRET` matches between frontend and backend
3. Verify token expiration time is reasonable (24 hours recommended)

### Issue: MCP Tools Cannot Call Phase 2 APIs

**Symptoms**: 403 errors or "user_id mismatch" errors

**Solution**:
1. Verify `API_BASE_URL` in `.env` points to correct backend
2. Check JWT token is being passed to MCP tools
3. Verify `user_id` extraction from JWT is correct
4. Test Phase 2 APIs directly with same JWT token

### Issue: Database Migration Failed

**Symptoms**: Tables not created, foreign key errors

**Solution**:
1. Check database connection: `psql $DATABASE_URL`
2. Verify Phase 2 tables exist (users, tasks)
3. Run migrations manually: `alembic upgrade head`
4. Check migration logs for errors

### Issue: Chat Interface Not Appearing

**Symptoms**: Chat button not visible or not clickable

**Solution**:
1. Check browser console for JavaScript errors
2. Verify ChatButton component is imported in dashboard
3. Check CSS/styling is not hiding button
4. Verify frontend build is up to date: `npm run build`

---

## Testing Checklist

Before considering Phase 3 complete, verify:

### Backend Tests

- [ ] Database migrations applied successfully
- [ ] Conversation API endpoints work (create, list, get, delete)
- [ ] Message API endpoints work (create, list)
- [ ] MCP tools can call Phase 2 APIs with JWT
- [ ] AI agent can process messages and call tools
- [ ] OpenRouter API integration works
- [ ] JWT token validation works
- [ ] User isolation enforced (cannot access other users' conversations)

### Frontend Tests

- [ ] Chat button appears on dashboard
- [ ] Chat interface opens and closes
- [ ] Messages display correctly (user vs AI styling)
- [ ] User can send messages
- [ ] AI responses appear
- [ ] Conversation history loads
- [ ] Phase 2 task list updates when AI creates tasks
- [ ] Chat interface is responsive (mobile, tablet, desktop)

### Integration Tests

- [ ] User can create task via chat
- [ ] User can list tasks via chat
- [ ] User can complete task via chat
- [ ] User can update task via chat
- [ ] User can delete task via chat (with confirmation)
- [ ] AI handles ambiguous input gracefully
- [ ] AI handles errors gracefully (API failures, invalid input)
- [ ] Phase 2 functionality unchanged (can still use UI without chat)

---

## Development Tips

### Hot Reload

- **Backend**: `uvicorn --reload` automatically reloads on code changes
- **Frontend**: `npm run dev` automatically reloads on code changes

### Debugging

**Backend**:
```python
# Add logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("AI agent processing message: %s", message)
```

**Frontend**:
```typescript
// Add console logging
console.log("Sending message:", message);
console.log("AI response:", response);
```

### Database Inspection

```bash
# Connect to database
psql $DATABASE_URL

# View conversations
SELECT * FROM conversations ORDER BY updated_at DESC LIMIT 10;

# View messages
SELECT * FROM messages WHERE conversation_id = '<conversation-id>' ORDER BY created_at;

# Count messages per conversation
SELECT conversation_id, COUNT(*) FROM messages GROUP BY conversation_id;
```

---

## Next Steps

After completing development:

1. **Run Tests**: Execute all unit, integration, and E2E tests
2. **Code Review**: Review code against constitution principles
3. **Documentation**: Update README with Phase 3 features
4. **Deployment**: Deploy to staging environment
5. **User Testing**: Conduct user acceptance testing
6. **Production**: Deploy to production after approval

---

## Additional Resources

- **OpenSDK Documentation**: [opensdk.dev](https://opensdk.dev)
- **OpenRouter Documentation**: [openrouter.ai/docs](https://openrouter.ai/docs)
- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Phase 2 Documentation**: See `../002-auth-landing/` for Phase 2 setup
- **Constitution**: See `.specify/memory/constitution.md` for project principles

---

**Quickstart Status**: ✅ Complete
**Ready for**: Development and Testing
