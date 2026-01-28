# Research & Technical Decisions: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2026-01-24
**Status**: Complete

## Overview

This document captures technical research and decisions made during Phase 0 planning for the AI-powered Todo Chatbot feature. All decisions align with Phase 3 Constitution principles and the approved feature specification.

---

## 1. OpenSDK Integration with OpenRouter

### Decision: Use OpenSDK with OpenRouter as LLM Provider

**Research Question**: How to configure OpenSDK to use OpenRouter for LLM inference while maintaining free-tier compatibility?

**Options Considered**:
1. OpenSDK + OpenRouter (free-tier models)
2. OpenSDK + Local LLM (Ollama)
3. LangChain + OpenRouter
4. Custom agent implementation

**Decision**: OpenSDK + OpenRouter with free-tier model

**Rationale**:
- **Constitution Requirement**: Principle VII mandates OpenSDK with OpenRouter
- **Free-tier Access**: OpenRouter provides free-tier models (meta-llama/llama-3.2-3b-instruct:free)
- **Standardization**: OpenSDK provides standardized agent orchestration
- **Tool Support**: Native MCP tool integration
- **Cost**: Zero inference cost with free-tier models

**Implementation Details**:
- OpenRouter API Key: Stored in backend `.env` as `OPENROUTER_API_KEY`
- Model Selection: `meta-llama/llama-3.2-3b-instruct:free`
- Authentication: API key in request headers (`Authorization: Bearer {api_key}`)
- Rate Limits: Free-tier limits apply (handle gracefully with retries)
- Error Handling: Catch API errors, return user-friendly messages

**Configuration Example**:
```python
from opensdk import Agent

agent = Agent(
    model="meta-llama/llama-3.2-3b-instruct:free",
    provider="openrouter",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    tools=[list_tasks, create_task, get_task, update_task, delete_task, complete_task]
)
```

**Alternatives Rejected**:
- Local LLM (Ollama): Requires local GPU resources, deployment complexity
- LangChain: Not mandated by constitution, OpenSDK preferred
- Custom implementation: Reinventing the wheel, OpenSDK provides needed features

---

## 2. MCP Tool Implementation Pattern

### Decision: HTTP-based MCP Tools with JWT Propagation

**Research Question**: How should MCP tools interact with Phase 2 APIs while maintaining security and isolation?

**Options Considered**:
1. HTTP requests to Phase 2 APIs (with JWT)
2. Direct function calls to Phase 2 services
3. Shared database access
4. Message queue (async)

**Decision**: HTTP requests to Phase 2 APIs with JWT token propagation

**Rationale**:
- **Constitution Requirement**: Principle VIII mandates HTTP-based tool-to-API mapping
- **Isolation**: AI agent never accesses database directly (Principle VII)
- **Security**: JWT token ensures authentication and authorization
- **Immutability**: Phase 2 APIs unchanged (Principle X)
- **Consistency**: AI uses same APIs as frontend

**Implementation Pattern**:
```python
import httpx

def create_task_tool(title: str, description: str, jwt_token: str) -> dict:
    """MCP tool to create a task via Phase 2 API"""
    # Extract user_id from JWT token
    user_id = extract_user_id_from_jwt(jwt_token)

    # Call Phase 2 API
    response = httpx.post(
        f"{API_BASE_URL}/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"title": title, "description": description}
    )

    # Handle response
    if response.status_code == 201:
        return {"success": True, "task": response.json()}
    else:
        return {"success": False, "error": response.json().get("detail")}
```

**Key Design Decisions**:
- JWT token passed to tools from conversation API context
- Tools extract `user_id` from JWT (not from AI input)
- Tools validate inputs before API calls
- Tools return structured responses (not raw HTTP)
- Tools handle API errors gracefully

**Alternatives Rejected**:
- Direct function calls: Violates isolation principle, bypasses authorization
- Database access: Violates Principle VII (AI never accesses DB)
- Message queue: Unnecessary complexity for synchronous operations

---

## 3. Conversation State Management

### Decision: Database-Persisted Conversations with Stateless Backend

**Research Question**: How to manage conversation history while maintaining backend statelessness?

**Options Considered**:
1. Database persistence (load on each request)
2. In-memory session storage
3. Client-side storage only
4. Redis cache with DB fallback

**Decision**: Database persistence with per-request history loading

**Rationale**:
- **Constitution Requirement**: Principle VII mandates stateless backend
- **Persistence**: Conversation history survives server restarts
- **User Isolation**: Database foreign keys enforce security
- **Scalability**: No server-side session state
- **Multi-turn Context**: Load recent messages for AI context

**Database Schema**:
- `conversations` table: user_id, title, created_at, updated_at
- `messages` table: conversation_id, role, content, created_at
- Foreign keys: conversations.user_id → users.id, messages.conversation_id → conversations.id
- Indexes: user_id, conversation_id, created_at

**Context Loading Strategy**:
- Load last N messages (e.g., 20) from database on each request
- Pass messages to OpenSDK as conversation history
- LLM uses history for context-aware responses
- Pagination for older messages if needed

**Performance Optimization**:
- Index on (conversation_id, created_at) for fast message retrieval
- Limit context window to prevent LLM token overflow
- Consider caching recent conversations (future optimization)

**Alternatives Rejected**:
- In-memory sessions: Violates stateless requirement, not scalable
- Client-side only: Loses history on page refresh, no server-side context
- Redis cache: Unnecessary complexity for MVP, can add later

---

## 4. Frontend Chat UI Pattern

### Decision: Modal Overlay with Conversation Sidebar

**Research Question**: What UI pattern best supports optional, non-intrusive chat while maintaining Phase 2 functionality?

**Options Considered**:
1. Modal overlay (centered)
2. Slide-in panel (right side)
3. Bottom sheet (mobile-first)
4. Inline chat (replaces task list)

**Decision**: Slide-in panel from right side (desktop) / bottom sheet (mobile)

**Rationale**:
- **Non-intrusive**: Overlays dashboard, doesn't replace Phase 2 UI
- **Optional**: Easily dismissed, Phase 2 works without it
- **Responsive**: Adapts to screen size (panel on desktop, sheet on mobile)
- **Conversation History**: Sidebar shows past conversations
- **Modern UX**: Common pattern in chat applications

**UI Components**:
- **ChatButton**: Floating button (bottom-right) or header button
- **ChatInterface**: Slide-in panel (400-500px wide on desktop)
- **ConversationList**: Sidebar within panel showing past conversations
- **ChatMessage**: Individual message component (user vs assistant styling)
- **MessageInput**: Text input with send button at bottom

**Responsive Behavior**:
- Desktop (>1024px): Slide-in panel from right, 400px wide
- Tablet (768-1024px): Slide-in panel from right, 350px wide
- Mobile (<768px): Bottom sheet, full width, 70% height

**State Management**:
- Current conversation ID stored in React state
- Messages loaded from API on conversation switch
- Real-time updates via polling (every 2-3 seconds while open)
- WebSocket upgrade (future enhancement)

**Alternatives Rejected**:
- Modal (centered): Takes too much screen space, blocks task list
- Inline chat: Replaces Phase 2 UI, violates optional requirement
- Full-page chat: Not optional, breaks Phase 2 workflow

---

## 5. Authentication & JWT Token Handling

### Decision: Reuse Phase 2 JWT with Token Propagation

**Research Question**: How to authenticate AI agent requests while maintaining Phase 2 immutability?

**Options Considered**:
1. Reuse Phase 2 JWT (propagate through layers)
2. Separate AI service token
3. API key for AI agent
4. Service-to-service authentication

**Decision**: Reuse Phase 2 JWT, propagate through all layers

**Rationale**:
- **Immutability**: No changes to Phase 2 authentication (Principle X)
- **User Context**: JWT contains user_id for authorization
- **Consistency**: Same token used by frontend, conversation API, MCP tools
- **Security**: Existing JWT validation logic reused

**Token Flow**:
1. Frontend: User authenticated via Phase 2 Better Auth
2. Frontend: Stores JWT token (httpOnly cookie or localStorage)
3. Frontend: Includes token in conversation API requests
4. Backend: Conversation API validates JWT, extracts user_id
5. Backend: Passes JWT to AI agent context
6. AI Agent: Provides JWT to MCP tools
7. MCP Tools: Include JWT in Phase 2 API requests
8. Phase 2 APIs: Validate JWT (existing logic, unchanged)

**Token Extraction in MCP Tools**:
```python
import jwt

def extract_user_id_from_jwt(token: str) -> str:
    """Extract user_id from JWT token"""
    try:
        payload = jwt.decode(
            token,
            os.getenv("BETTER_AUTH_SECRET"),
            algorithms=["HS256"]
        )
        return payload["user_id"]
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid JWT token")
```

**Token Expiration Handling**:
- Frontend detects 401 errors from conversation API
- Prompts user to re-authenticate
- Redirects to login page if token expired

**Alternatives Rejected**:
- Separate AI token: Unnecessary complexity, duplicate auth logic
- API key: Doesn't provide user context, requires separate authorization
- Service auth: Bypasses user-level authorization, security risk

---

## 6. Error Handling & Graceful Degradation

### Decision: Multi-Layer Error Handling with Fallback to Phase 2 UI

**Research Question**: How to handle AI service failures without breaking user experience?

**Strategy**:
1. **OpenRouter API Errors**: Retry with exponential backoff, show error message
2. **MCP Tool Failures**: Return error to AI, AI generates explanation
3. **Phase 2 API Errors**: Pass through to AI, AI explains to user
4. **Network Errors**: Show connection error, suggest retry
5. **Token Expiration**: Prompt re-authentication

**Error Messages**:
- User-friendly: "I'm having trouble connecting. Please try again."
- Actionable: "Your session expired. Please log in again."
- Fallback: "You can also manage tasks using the task list above."

**Graceful Degradation**:
- If AI unavailable: Phase 2 UI still fully functional
- If conversation API down: Phase 2 task management unaffected
- If database error: Show error, don't crash application

**Monitoring & Logging**:
- Log all AI agent errors for debugging
- Track OpenRouter API response times
- Monitor MCP tool success rates
- Alert on high error rates

---

## 7. Performance Optimization

### Decision: Optimize for < 3 Second AI Response Time

**Research Question**: How to meet SC-005 success criteria (AI responses within 3 seconds)?

**Optimization Strategies**:
1. **Model Selection**: Use fast free-tier model (llama-3.2-3b)
2. **Context Limiting**: Load only recent 20 messages
3. **Parallel Processing**: MCP tool calls can be parallelized by OpenSDK
4. **Database Indexing**: Index on conversation_id, created_at
5. **Connection Pooling**: Reuse HTTP connections for API calls

**Performance Targets**:
- OpenRouter API call: < 2 seconds
- Database queries: < 100ms
- MCP tool execution: < 500ms
- Total response time: < 3 seconds

**Monitoring**:
- Track P95 response times
- Alert if > 3 seconds consistently
- Optimize slow queries

**Future Enhancements**:
- Caching frequent queries
- Streaming responses (show partial AI output)
- WebSocket for real-time updates

---

## 8. Testing Strategy

### Decision: Multi-Layer Testing (Unit, Integration, E2E)

**Test Coverage**:
1. **Unit Tests**: MCP tools, conversation service, database models
2. **Integration Tests**: Conversation API endpoints, AI agent with mock tools
3. **E2E Tests**: Full conversation flow (user message → AI response)
4. **Contract Tests**: Verify MCP tools match Phase 2 API contracts

**Key Test Scenarios**:
- User creates task via chat
- User lists tasks via chat
- User completes task via chat
- AI handles ambiguous input
- AI handles non-existent task
- Token expiration during chat
- OpenRouter API failure
- Phase 2 API error handling

**Testing Tools**:
- Backend: pytest, pytest-asyncio
- Frontend: Jest, React Testing Library
- E2E: Playwright or Cypress
- API: Postman/Newman for contract tests

---

## Summary of Key Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| AI Framework | OpenSDK + OpenRouter | Constitution mandate, free-tier access |
| LLM Model | meta-llama/llama-3.2-3b-instruct:free | Free, fast, sufficient for task management |
| Tool Protocol | HTTP-based MCP tools | Isolation, security, Phase 2 immutability |
| State Management | Database-persisted, stateless backend | Scalability, persistence, constitution compliance |
| Frontend UI | Slide-in panel / bottom sheet | Non-intrusive, optional, responsive |
| Authentication | Reuse Phase 2 JWT | Immutability, consistency, security |
| Error Handling | Multi-layer with graceful degradation | User experience, reliability |
| Performance | < 3 second response time | Success criteria SC-005 |

---

**Research Status**: ✅ Complete
**Next Phase**: Phase 1 - Data Model & Contracts
