# Implementation Plan: AI-Powered Todo Chatbot

**Branch**: `003-ai-chatbot` | **Date**: 2026-01-24 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot/spec.md`

## Summary

Phase 3 adds conversational AI capabilities to the existing Phase 2 Todo application, enabling users to manage tasks through natural language chat interactions. The AI agent, orchestrated by OpenSDK with OpenRouter as the LLM provider, interacts with Phase 2 REST APIs exclusively through MCP tools, maintaining strict isolation from the database and preserving Phase 2 immutability. Conversations are persisted in new database tables, the backend remains stateless, and the chat interface is optional (button-triggered modal/panel).

## Technical Context

**Language/Version**:
- Backend: Python 3.11+ (existing Phase 2)
- Frontend: TypeScript with Next.js 16 (existing Phase 2)
- AI Layer: Python 3.11+ (new Phase 3 component)

**Primary Dependencies**:
- **AI Orchestration**: OpenSDK (agent framework)
- **LLM Provider**: OpenRouter API (free-tier models: meta-llama/llama-3.2-3b-instruct:free)
- **Tool Protocol**: MCP (Model Context Protocol) for tool definitions
- **Backend**: FastAPI (existing), SQLModel (existing), PyJWT (existing)
- **Frontend**: React, Axios (existing), shadcn/ui (existing)
- **HTTP Client**: httpx or requests (for MCP tools calling Phase 2 APIs)

**Storage**:
- Neon PostgreSQL (existing Phase 2)
- New tables: conversations, messages (Phase 3 additions)

**Testing**:
- Backend: pytest (existing)
- Frontend: Jest/React Testing Library (existing)
- Integration: End-to-end conversation flow tests

**Target Platform**:
- Backend: Linux server / Cloud hosting (existing)
- Frontend: Web browsers (desktop and mobile)
- AI Agent: Server-side Python process

**Project Type**: Web application (frontend + backend + ai-agent)

**Performance Goals**:
- AI response time: < 3 seconds (per success criteria SC-005)
- Chat interface open/close: < 1 second (per SC-004)
- Task creation via chat: < 30 seconds total (per SC-001)
- Conversation history retrieval: < 2 seconds (per SC-010)

**Constraints**:
- AI agent MUST NOT access database directly (Constitution Principle VII)
- MCP tools MUST call Phase 2 APIs via HTTP (Constitution Principle VIII)
- Backend MUST remain stateless (Constitution Principle VII)
- Phase 2 code MUST NOT be modified (Constitution Principle X)
- Only free-tier LLM models allowed (Constitution Principle VII)

**Scale/Scope**:
- Support existing Phase 2 user base
- Conversation history per user (unbounded, subject to data retention policies)
- Multi-turn conversations with context awareness
- 6 MCP tools mapping to 6 Phase 2 task API endpoints

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-First Development ✅
- [x] Feature specification approved (specs/003-ai-chatbot/spec.md)
- [x] Planning follows specification requirements
- [x] No code written before plan approval

### Principle II: Security-First Architecture ✅
- [x] All API calls include JWT token (MCP tools will include Authorization header)
- [x] User isolation maintained (MCP tools extract user_id from JWT)
- [x] No secrets in code (OPENROUTER_API_KEY in .env)

### Principle III: Full-Stack Type Safety ✅
- [x] TypeScript for frontend chat components (strict mode)
- [x] Python type hints for AI agent and MCP tools
- [x] SQLModel for new database models (conversations, messages)

### Principle IV: Environment-Based Configuration ✅
- [x] New environment variable: OPENROUTER_API_KEY (backend .env)
- [x] Existing variables reused: BETTER_AUTH_SECRET, DATABASE_URL
- [x] .env.example updated with new variable

### Principle V: Responsive Design ✅
- [x] Chat interface responsive (mobile-first)
- [x] Modal/slide-in panel adapts to screen size
- [x] Touch targets minimum 44x44px

### Principle VI: API Contract Compliance ✅
- [x] Phase 2 APIs unchanged (read-only access via MCP tools)
- [x] New conversation APIs follow Phase 2 patterns
- [x] All endpoints require JWT authentication

### Principle VII: AI Integration Architecture (NON-NEGOTIABLE) ✅
- [x] OpenSDK used for agent orchestration
- [x] OpenRouter configured as LLM provider
- [x] Free-tier model: meta-llama/llama-3.2-3b-instruct:free
- [x] AI agent NEVER accesses database directly
- [x] AI agent uses ONLY MCP tools
- [x] Backend remains stateless
- [x] Conversations persisted in database

### Principle VIII: MCP Tool Design (NON-NEGOTIABLE) ✅
- [x] 6 MCP tools map 1-to-1 to Phase 2 task APIs
- [x] Tools call APIs via HTTP (not direct function calls)
- [x] Tools include JWT token in requests
- [x] Tools extract user_id from JWT (not parameter)
- [x] Tools return structured responses
- [x] Tools delegate business logic to APIs

### Principle IX: Conversation Management ✅
- [x] Conversations stored in database
- [x] Messages stored with role, content, timestamp
- [x] User isolation maintained
- [x] New conversation APIs follow Phase 2 patterns

### Principle X: Phase 2 Immutability (NON-NEGOTIABLE) ✅
- [x] Phase 2 APIs not modified
- [x] Phase 2 database schema (users, tasks) not modified
- [x] Phase 2 authentication not modified
- [x] Phase 3 features additive only
- [x] Chat interface optional (button-triggered)

**Constitution Check Result**: ✅ PASSED - All principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technical decisions)
├── data-model.md        # Phase 1 output (database schema)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (API contracts)
│   ├── conversation-api.yaml    # Conversation management endpoints
│   └── mcp-tools.yaml           # MCP tool definitions
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py              # Existing Phase 2
│   │   ├── task.py              # Existing Phase 2
│   │   ├── conversation.py      # NEW Phase 3
│   │   └── message.py           # NEW Phase 3
│   ├── api/
│   │   ├── auth.py              # Existing Phase 2
│   │   ├── tasks.py             # Existing Phase 2 (unchanged)
│   │   └── conversations.py     # NEW Phase 3
│   ├── services/
│   │   ├── auth_service.py      # Existing Phase 2
│   │   ├── task_service.py      # Existing Phase 2 (unchanged)
│   │   └── conversation_service.py  # NEW Phase 3
│   └── middleware/
│       └── auth.py              # Existing Phase 2 (reused)
├── ai_agent/                    # NEW Phase 3 - AI agent module
│   ├── __init__.py
│   ├── agent.py                 # OpenSDK agent initialization
│   ├── tools/                   # MCP tool implementations
│   │   ├── __init__.py
│   │   ├── list_tasks.py
│   │   ├── create_task.py
│   │   ├── get_task.py
│   │   ├── update_task.py
│   │   ├── delete_task.py
│   │   └── complete_task.py
│   └── config.py                # OpenRouter configuration
└── tests/
    ├── test_conversations.py    # NEW Phase 3
    └── test_mcp_tools.py        # NEW Phase 3

frontend/
├── src/
│   ├── components/
│   │   ├── TaskList.tsx         # Existing Phase 2
│   │   ├── TaskForm.tsx         # Existing Phase 2
│   │   ├── ChatButton.tsx       # NEW Phase 3
│   │   ├── ChatInterface.tsx    # NEW Phase 3
│   │   ├── ChatMessage.tsx      # NEW Phase 3
│   │   └── ConversationList.tsx # NEW Phase 3
│   ├── pages/
│   │   └── dashboard.tsx        # Existing Phase 2 (add ChatButton)
│   ├── services/
│   │   ├── taskService.ts       # Existing Phase 2 (unchanged)
│   │   └── chatService.ts       # NEW Phase 3
│   └── hooks/
│       └── useChat.ts           # NEW Phase 3
└── tests/
    └── chat.test.tsx            # NEW Phase 3
```

**Structure Decision**: Web application structure (Option 2) with Phase 3 additions. Backend adds `ai_agent/` module for OpenSDK agent and MCP tools, new API endpoints for conversations, and new database models. Frontend adds chat UI components. Phase 2 code remains unchanged except for adding ChatButton to dashboard.

## Complexity Tracking

> No constitution violations - this section is empty.

---

## Phase 0: Research & Technical Decisions

### Research Areas

1. **OpenSDK Integration with OpenRouter**
   - How to configure OpenSDK to use OpenRouter as provider
   - Authentication mechanism for OpenRouter API
   - Free-tier model selection and limitations
   - Error handling for API rate limits

2. **MCP Tool Implementation**
   - MCP tool definition format and schema
   - How OpenSDK discovers and registers tools
   - Tool parameter validation and error handling
   - JWT token extraction and forwarding in tools

3. **Conversation State Management**
   - Database schema for conversations and messages
   - Conversation context loading for multi-turn interactions
   - Message ordering and pagination
   - Conversation history retrieval patterns

4. **Frontend Chat UI Patterns**
   - Modal vs slide-in panel for chat interface
   - Real-time message updates (polling vs WebSocket)
   - Message rendering and formatting
   - Loading states and error handling

### Research Outputs

See [research.md](./research.md) for detailed findings and decisions.

---

## Phase 1: Design & Contracts

### Data Models

See [data-model.md](./data-model.md) for complete schema definitions.

**Summary**:
- **Conversation**: user_id (FK), title (optional), created_at, updated_at
- **Message**: conversation_id (FK), role (user/assistant), content, created_at

### API Contracts

See [contracts/](./contracts/) for OpenAPI specifications.

**New Endpoints**:
- `GET /api/{user_id}/conversations` - List user's conversations
- `POST /api/{user_id}/conversations` - Create new conversation
- `GET /api/{user_id}/conversations/{id}` - Get conversation details
- `GET /api/{user_id}/conversations/{id}/messages` - Get conversation messages
- `POST /api/{user_id}/conversations/{id}/messages` - Add message to conversation

**MCP Tools** (defined in contracts/mcp-tools.yaml):
- `list_tasks` - Calls GET /api/{user_id}/tasks
- `create_task` - Calls POST /api/{user_id}/tasks
- `get_task` - Calls GET /api/{user_id}/tasks/{id}
- `update_task` - Calls PUT /api/{user_id}/tasks/{id}
- `delete_task` - Calls DELETE /api/{user_id}/tasks/{id}
- `complete_task` - Calls PATCH /api/{user_id}/tasks/{id}/complete

### Setup Instructions

See [quickstart.md](./quickstart.md) for development setup.

---

## Architecture Overview

### Component Interaction Flow

```
User Input (Frontend)
    ↓
[ChatInterface Component]
    ↓ HTTP POST /api/{user_id}/conversations/{id}/messages
[Backend: Conversation API]
    ↓ Save user message to DB
    ↓ Forward to AI Agent
[OpenSDK Agent]
    ↓ Process natural language
    ↓ Determine intent & select tool
[MCP Tool (e.g., create_task)]
    ↓ Extract user_id from JWT
    ↓ HTTP POST /api/{user_id}/tasks (with JWT)
[Phase 2 Task API]
    ↓ Validate JWT & user_id
    ↓ Create task in DB
    ↓ Return task data
[MCP Tool]
    ↓ Format response for AI
[OpenSDK Agent]
    ↓ Generate natural language response
[Backend: Conversation API]
    ↓ Save assistant message to DB
    ↓ Return response
[ChatInterface Component]
    ↓ Display AI response
User sees confirmation
```

### Data Flow Details

**1. User Sends Message**
- Frontend: User types message in ChatInterface
- Frontend: POST /api/{user_id}/conversations/{conversation_id}/messages
  - Headers: Authorization: Bearer {jwt_token}
  - Body: { role: "user", content: "Create a task to buy groceries" }
- Backend: Conversation API validates JWT, extracts user_id
- Backend: Saves message to messages table
- Backend: Forwards message to OpenSDK agent

**2. AI Agent Processes Message**
- OpenSDK: Loads conversation history from database
- OpenSDK: Sends message + history to OpenRouter LLM
- LLM: Analyzes intent, determines action needed
- LLM: Selects appropriate MCP tool (e.g., create_task)
- LLM: Generates tool parameters from natural language

**3. MCP Tool Executes**
- Tool: Receives parameters from OpenSDK
- Tool: Extracts user_id from JWT token (passed from original request)
- Tool: Validates parameters
- Tool: Makes HTTP request to Phase 2 API
  - URL: POST http://backend:8000/api/{user_id}/tasks
  - Headers: Authorization: Bearer {jwt_token}
  - Body: { title: "Buy groceries", description: "" }
- Phase 2 API: Validates JWT, checks user_id match
- Phase 2 API: Creates task in database
- Phase 2 API: Returns task data
- Tool: Formats response for AI agent
- Tool: Returns structured result to OpenSDK

**4. AI Agent Generates Response**
- OpenSDK: Receives tool execution result
- OpenSDK: Sends result to OpenRouter LLM
- LLM: Generates natural language confirmation
- OpenSDK: Returns response to backend

**5. Backend Saves and Returns Response**
- Backend: Saves assistant message to messages table
  - conversation_id, role: "assistant", content: "I've created a task..."
- Backend: Returns response to frontend
- Frontend: Displays message in ChatInterface
- Frontend: Updates conversation history

### Authentication & Authorization Flow

**JWT Token Propagation**:
1. User authenticates via Phase 2 Better Auth (unchanged)
2. Frontend stores JWT token (httpOnly cookie or localStorage)
3. Frontend includes token in all API requests: `Authorization: Bearer {token}`
4. Backend conversation API validates token, extracts user_id
5. Backend passes token to AI agent context
6. MCP tools extract user_id from token
7. MCP tools include token in Phase 2 API calls
8. Phase 2 APIs validate token and user_id (existing logic, unchanged)

**User Isolation**:
- Conversation API filters conversations by user_id from JWT
- Message API filters messages by conversation ownership
- MCP tools extract user_id from JWT (not from AI input)
- Phase 2 APIs enforce user_id validation (existing, unchanged)

### Stateless Backend Design

**No Server-Side Sessions**:
- Each API request independently authenticated via JWT
- No in-memory conversation state
- AI agent loads conversation history from database on each request
- OpenSDK agent instance created per request (or pooled, but stateless)

**Conversation Context Loading**:
- When user sends message, backend loads recent messages from database
- Messages passed to OpenSDK as conversation history
- LLM uses history for context-aware responses
- No state persisted between requests

### Frontend Chat Integration

**Chat Button Placement**:
- Add ChatButton component to dashboard header (Phase 2 page)
- Button styled consistently with Phase 2 UI (shadcn/ui)
- Button position: floating (bottom-right) or header (top-right)

**Chat Interface Behavior**:
- Click button → open modal or slide-in panel
- Interface overlays dashboard (does not replace it)
- Close button → dismiss interface, return to dashboard
- Phase 2 task list remains functional while chat is open
- Chat and task list stay synchronized (both read from same APIs)

**Conversation Management**:
- On first open: create new conversation automatically
- Display conversation history in sidebar or dropdown
- Allow switching between conversations
- Current conversation persists across page refreshes (stored in DB)

---

## Phase 2 and Phase 3 Separation

### Phase 2 Responsibilities (Unchanged)

**Backend**:
- User authentication (Better Auth + JWT)
- Task CRUD operations (6 REST API endpoints)
- Database access (users, tasks tables)
- Authorization (user_id validation)

**Frontend**:
- Landing page
- Authentication pages (login, register)
- Dashboard with task list
- Task forms (create, edit)
- Task UI interactions (checkboxes, buttons)

**Database**:
- users table
- tasks table

### Phase 3 Responsibilities (New)

**Backend**:
- Conversation CRUD operations (4 new REST API endpoints)
- Message persistence
- AI agent orchestration (OpenSDK)
- MCP tool implementations (6 tools)
- OpenRouter API integration

**Frontend**:
- Chat button component
- Chat interface (modal/panel)
- Message display components
- Conversation list component
- Chat service (API client)

**Database**:
- conversations table (new)
- messages table (new)

**AI Layer**:
- OpenSDK agent configuration
- Natural language understanding
- Tool selection and execution
- Response generation

### Integration Points

**Frontend**:
- Dashboard page: add ChatButton component (minimal change)
- Shared authentication: reuse existing JWT token
- Shared styling: use existing shadcn/ui components

**Backend**:
- Shared authentication middleware: reuse JWT validation
- Shared database connection: extend with new tables
- MCP tools call Phase 2 APIs: HTTP requests with JWT

**Database**:
- New tables reference users table via foreign key
- No changes to existing tables

---

## Risk Analysis

### Technical Risks

1. **OpenRouter API Availability**
   - Risk: Free-tier rate limits or service downtime
   - Mitigation: Implement retry logic, graceful error messages, fallback to Phase 2 UI

2. **AI Response Quality**
   - Risk: Free-tier model may misinterpret user intent
   - Mitigation: Clear error messages, allow user to rephrase, provide examples

3. **JWT Token Expiration During Chat**
   - Risk: Token expires mid-conversation
   - Mitigation: Frontend detects 401 errors, prompts re-authentication

4. **Conversation History Size**
   - Risk: Large conversation history may exceed LLM context window
   - Mitigation: Load only recent N messages, implement pagination

### Security Risks

1. **AI Prompt Injection**
   - Risk: User crafts input to manipulate AI behavior
   - Mitigation: Sanitize inputs, limit AI to task management domain, validate tool outputs

2. **Unauthorized API Access via Tools**
   - Risk: MCP tools bypass authorization
   - Mitigation: Tools extract user_id from JWT, Phase 2 APIs validate independently

3. **Conversation Data Leakage**
   - Risk: User accesses another user's conversations
   - Mitigation: Conversation APIs filter by user_id from JWT, database foreign keys enforce isolation

---

## Next Steps

1. **Review this plan** for completeness and accuracy
2. **Approve plan** before proceeding to task generation
3. **Run `/sp.tasks`** to generate implementation tasks
4. **Execute tasks** via Claude Code following Spec-Driven Development workflow

---

**Plan Status**: ✅ Complete - Ready for review and approval
**Next Command**: `/sp.tasks` (after plan approval)
