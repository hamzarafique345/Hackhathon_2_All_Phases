---
id: 002
title: AI Chatbot Implementation Plan
stage: plan
date: 2026-01-24
surface: agent
model: claude-sonnet-4-5
feature: ai-chatbot
branch: 003-ai-chatbot
user: unknown
command: /sp.plan
labels: ["plan", "ai-chatbot", "phase3", "opensdk", "openrouter", "mcp-tools", "architecture"]
links:
  spec: specs/003-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-ai-chatbot/plan.md
  - specs/003-ai-chatbot/research.md
  - specs/003-ai-chatbot/data-model.md
  - specs/003-ai-chatbot/contracts/conversation-api.yaml
  - specs/003-ai-chatbot/contracts/mcp-tools.md
  - specs/003-ai-chatbot/quickstart.md
tests:
  - none
---

## Prompt

Generate a Phase 3 implementation plan based strictly on the approved Constitution and Specification.

Context:
- Phase 2 code already exists and must be reused.
- Phase 3 introduces an AI chatbot layer.
- OpenSDK must be used to manage AI agents and tool execution.
- OpenRouter must be used as the LLM provider with free-tier models.
- MCP tools provide controlled access to Phase 2 APIs.

Plan Requirements:
- Describe how OpenSDK agents interact with MCP tools.
- Describe the data flow from user input to AI response.
- Explain how chat requests are authenticated and authorized.
- Explain conversation persistence and stateless backend handling.
- Describe frontend chat integration (button-triggered chat UI).
- Clearly separate Phase 2 and Phase 3 responsibilities.

Constraints:
- Do NOT write code.
- Do NOT generate tasks.
- Do NOT repeat specification text.

Output:
- A clear, step-by-step technical plan.
- Written for both human reviewers and AI agents.

## Response snapshot

Created comprehensive Phase 3 implementation plan with complete architecture, data models, API contracts, and development setup.

**Main Plan Document (plan.md)**:
- Summary of Phase 3 approach (OpenSDK + OpenRouter + MCP tools)
- Technical context (Python 3.11+, TypeScript, OpenSDK, OpenRouter, free-tier models)
- Constitution check (all 10 principles validated and passed)
- Project structure (backend ai_agent/ module, frontend chat components)
- Architecture overview with detailed component interaction flow
- Data flow from user input → AI response (8-step process)
- Authentication & authorization flow (JWT token propagation)
- Stateless backend design (database-persisted conversations)
- Frontend chat integration (slide-in panel, responsive)
- Phase 2/Phase 3 separation (clear boundaries, no Phase 2 modifications)
- Risk analysis (technical and security risks with mitigations)

**Research Document (research.md)**:
- OpenSDK + OpenRouter integration (free-tier model selection)
- MCP tool implementation pattern (HTTP-based with JWT)
- Conversation state management (database-persisted, stateless)
- Frontend chat UI pattern (slide-in panel/bottom sheet)
- Authentication & JWT handling (token propagation through layers)
- Error handling & graceful degradation (multi-layer strategy)
- Performance optimization (< 3 second response time target)
- Testing strategy (unit, integration, E2E, contract tests)

**Data Model Document (data-model.md)**:
- Database schema for conversations and messages tables
- SQLModel definitions (Python ORM models)
- Pydantic DTOs for API requests/responses
- Data validation rules and business logic
- Alembic migration script
- Query patterns and performance considerations

**API Contracts**:
- conversation-api.yaml: OpenAPI 3.0 spec for 4 conversation endpoints
- mcp-tools.md: 6 MCP tool definitions mapping to Phase 2 APIs
  - list_tasks, create_task, get_task, update_task, complete_task, delete_task
  - Each tool includes parameters, implementation pattern, response format, error handling

**Quickstart Guide (quickstart.md)**:
- Prerequisites (Node.js, Python, PostgreSQL, OpenRouter API key)
- Environment setup (backend and frontend)
- Database migration instructions
- Development workflow (verify Phase 2, test APIs, test MCP tools, test AI agent)
- Common issues & troubleshooting
- Testing checklist (backend, frontend, integration)
- Development tips (hot reload, debugging, database inspection)

**Key Architectural Decisions**:
1. **AI Isolation**: AI agent never accesses database directly, only through MCP tools
2. **Tool-to-API Mapping**: 1-to-1 mapping of MCP tools to Phase 2 REST APIs via HTTP
3. **JWT Propagation**: Token flows from frontend → conversation API → AI agent → MCP tools → Phase 2 APIs
4. **Stateless Backend**: Conversation history loaded from database on each request
5. **Phase 2 Immutability**: Zero modifications to Phase 2 code, APIs, or database schema
6. **Free-tier Model**: meta-llama/llama-3.2-3b-instruct:free via OpenRouter
7. **Frontend Integration**: Slide-in panel (desktop) / bottom sheet (mobile), optional and non-intrusive

**Constitution Compliance**:
- ✅ All 10 principles validated and passed
- ✅ Principle VII (AI Integration): OpenSDK + OpenRouter + MCP tools + stateless
- ✅ Principle VIII (MCP Tools): 1-to-1 HTTP-based mapping with JWT
- ✅ Principle IX (Conversation Management): Database persistence, user isolation
- ✅ Principle X (Phase 2 Immutability): Additive only, no Phase 2 changes

## Outcome

- ✅ Impact: Complete Phase 3 implementation plan with architecture, data models, API contracts, and development setup. Plan provides clear technical guidance for implementing AI chatbot while maintaining Phase 2 immutability and constitution compliance.
- 🧪 Tests: No tests (planning phase - test strategy documented in research.md)
- 📁 Files: Created 6 planning artifacts (plan.md, research.md, data-model.md, 2 contract files, quickstart.md)
- 🔁 Next prompts: Run /sp.tasks to generate implementation tasks based on this plan
- 🧠 Reflection: Plan successfully balances technical requirements (OpenSDK, OpenRouter, MCP tools) with architectural constraints (AI isolation, stateless backend, Phase 2 immutability). Detailed data flow and component interaction diagrams provide clear implementation guidance. All constitution principles validated and passed.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully with all artifacts generated
- Graders run and results (PASS/FAIL): Constitution check PASSED (all 10 principles satisfied)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.tasks to validate that plan provides sufficient detail for task generation and implementation
