---
id: 002
title: Phase 3 Constitution AI Integration Principles
stage: constitution
date: 2026-01-24
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 003-ai-chatbot
user: unknown
command: /sp.constitution
labels: ["constitution", "phase3", "ai-integration", "governance", "opensdk", "openrouter", "mcp-tools"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

Create a Phase 3 Constitution for the Todo project.

Context:
- Phase 2 (full-stack Todo application) is completed and stable.
- Phase 3 must extend Phase 2 without changing its behavior.
- All Phase 2 APIs, database schema, and authentication must remain unchanged.

Mandatory Rules:
- The project must follow strict Spec-Driven Development.
- No implementation is allowed before specifications are approved.
- AI integration must use OpenSDK for agent orchestration.
- OpenSDK must be configured to work with OpenRouter as the model provider.
- Only free-tier compatible models may be used.
- The AI must never access the database directly.
- The AI may interact with the system only through MCP tools.
- MCP tools must map one-to-one to existing Phase 2 REST APIs.
- The backend must be stateless.
- Conversation history must be persisted in the database.
- The chat interface must be optional and opened via a button.

Output Requirements:
- Produce a short, clear Constitution document.
- Focus on principles, constraints, and governance.

## Response snapshot

Updated constitution from v1.0.0 to v2.0.0 (MAJOR version bump).

**Key Changes**:
- Added 4 new Phase 3 principles (VII-X) for AI integration
- Preserved all 6 Phase 2 principles (I-VI) unchanged
- Added AI Stack section to Technology Stack
- Added Phase 3 database schema (conversations, messages tables)
- Added 3 new Quality Gates (AI Integration, Conversation, Phase 2 Immutability)
- Added AI Security section to Security Requirements

**New Principles**:
1. **Principle VII: AI Integration Architecture (NON-NEGOTIABLE)**
   - AI agent MUST use OpenSDK with OpenRouter
   - Only free-tier models allowed
   - AI MUST NEVER access database directly
   - AI MAY ONLY use MCP tools
   - Backend MUST remain stateless

2. **Principle VIII: MCP Tool Design (NON-NEGOTIABLE)**
   - Each MCP tool MUST map 1-to-1 to Phase 2 REST API
   - Tools MUST call APIs via HTTP (not direct function calls)
   - Tools MUST include JWT token in requests
   - Tools MUST extract user_id from token

3. **Principle IX: Conversation Management**
   - Conversations MUST be persisted in database
   - Messages MUST store role (user/assistant), content, timestamp
   - Conversation APIs MUST follow Phase 2 patterns
   - User isolation MUST be maintained

4. **Principle X: Phase 2 Immutability (NON-NEGOTIABLE)**
   - Phase 2 APIs MUST NOT be modified
   - Phase 2 database schema MUST NOT be modified
   - Phase 2 authentication MUST NOT be modified
   - Phase 3 features MUST be additive only
   - Chat interface MUST be optional

**Database Schema Additions**:
- conversations table (user_id FK, title, timestamps)
- messages table (conversation_id FK, role, content, timestamp)

**Version Bump Rationale**:
MAJOR bump (1.0.0 → 2.0.0) because:
- Introduces new architectural constraints (AI layer, MCP tools)
- Changes development approach (AI isolation requirements)
- Adds mandatory immutability constraint on Phase 2
- These are backward-incompatible governance changes

## Outcome

- ✅ Impact: Constitution updated with 4 new Phase 3 principles governing AI integration, MCP tool design, conversation management, and Phase 2 immutability. All Phase 2 principles preserved unchanged.
- 🧪 Tests: No tests (documentation update)
- 📁 Files: Updated .specify/memory/constitution.md (v1.0.0 → v2.0.0)
- 🔁 Next prompts: Ready to create Phase 3 feature specification using /sp.specify with AI chatbot requirements
- 🧠 Reflection: Constitution successfully establishes clear boundaries between Phase 2 (stable) and Phase 3 (AI extension). Key architectural decisions documented: OpenSDK+OpenRouter for AI, MCP tools for API access, database persistence for conversations, strict Phase 2 immutability.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution update completed successfully
- Graders run and results (PASS/FAIL): N/A (documentation update)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.specify to create AI chatbot feature specification following new constitution principles
