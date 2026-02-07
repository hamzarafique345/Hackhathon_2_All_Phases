---
description: "Task list for AI-Powered Todo Chatbot implementation"
---

# Tasks: AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/003-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, research.md

**Tests**: Tests are OPTIONAL - not included in this task list as they were not explicitly requested in the specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/ai_agent/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- **Database**: Migrations in `backend/alembic/versions/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [x] T001 [P] Install backend Phase 3 dependencies in backend/requirements.txt (opensdk, httpx, pyjwt)
- [x] T002 [P] Install frontend Phase 3 dependencies in frontend/package.json (@radix-ui/react-dialog, date-fns)
- [x] T003 [P] Update backend/.env.example with OPENROUTER_API_KEY placeholder
- [x] T004 [P] Create backend/ai_agent/ module directory structure (__init__.py, tools/, config.py, agent.py)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create Alembic migration for conversations table in backend/alembic/versions/003_add_conversations.py
- [x] T006 Create Alembic migration for messages table in backend/alembic/versions/003_add_messages.py
- [x] T007 [P] Create Conversation SQLModel in backend/src/models/conversation.py
- [x] T008 [P] Create Message SQLModel in backend/src/models/message.py
- [x] T009 [P] Create ConversationCreate Pydantic DTO in backend/src/models/conversation.py
- [x] T010 [P] Create ConversationResponse Pydantic DTO in backend/src/models/conversation.py
- [x] T011 [P] Create MessageCreate Pydantic DTO in backend/src/models/message.py
- [x] T012 [P] Create MessageResponse Pydantic DTO in backend/src/models/message.py
- [x] T013 Create ConversationService in backend/src/services/conversation_service.py
- [x] T014 Create JWT token extraction utility in backend/ai_agent/tools/__init__.py
- [x] T015 Configure OpenRouter API client in backend/ai_agent/config.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 6 - Chat Interface Access (Priority: P1) 🎯 MVP

**Goal**: Users can open and close the chat interface via a button, and the interface does not interfere with Phase 2 functionality

**Independent Test**: User can click a chat button to open the interface, interact with the AI, close the interface, and continue using the regular task management UI without any disruption

### Implementation for User Story 6

- [x] T016 [P] [US6] Create ChatButton component in frontend/src/components/ChatButton.tsx
- [x] T017 [P] [US6] Create ChatInterface component (modal/slide-in panel) in frontend/src/components/ChatInterface.tsx
- [x] T018 [P] [US6] Create ChatMessage component in frontend/src/components/ChatMessage.tsx
- [x] T019 [P] [US6] Create useChat custom hook in frontend/src/hooks/useChat.ts
- [x] T020 [US6] Add ChatButton to dashboard page in frontend/src/pages/dashboard.tsx
- [x] T021 [US6] Implement chat interface open/close state management in frontend/src/hooks/useChat.ts
- [x] T022 [US6] Style ChatInterface for responsive design (mobile, tablet, desktop) in frontend/src/components/ChatInterface.tsx

**Checkpoint**: At this point, User Story 6 should be fully functional - chat interface can be opened and closed without affecting Phase 2

---

## Phase 4: User Story 1 - Conversational Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks by describing them in natural language to the AI chatbot

**Independent Test**: User can open the chat interface, type "Add a task to buy groceries tomorrow", and see the task appear in their task list

### Implementation for User Story 1

- [x] T023 [P] [US1] Create list_tasks MCP tool in backend/ai_agent/tools/list_tasks.py
- [x] T024 [P] [US1] Create create_task MCP tool in backend/ai_agent/tools/create_task.py
- [x] T025 [P] [US1] Create get_task MCP tool in backend/ai_agent/tools/get_task.py
- [x] T026 [US1] Initialize OpenSDK agent with OpenRouter in backend/ai_agent/agent.py
- [x] T027 [US1] Register MCP tools with OpenSDK agent in backend/ai_agent/agent.py
- [x] T028 [US1] Create POST /api/{user_id}/conversations endpoint in backend/src/api/conversations.py
- [x] T029 [US1] Create POST /api/{user_id}/conversations/{id}/messages endpoint in backend/src/api/conversations.py
- [x] T030 [US1] Implement AI agent invocation in message creation endpoint in backend/src/api/conversations.py
- [x] T031 [US1] Create chatService.ts API client in frontend/src/services/chatService.ts
- [x] T032 [US1] Implement message sending in useChat hook in frontend/src/hooks/useChat.ts
- [x] T033 [US1] Connect ChatInterface to chatService for message creation in frontend/src/components/ChatInterface.tsx
- [x] T034 [US1] Display AI responses in ChatInterface in frontend/src/components/ChatInterface.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional - users can create tasks via chat and see them in the task list

---

## Phase 5: User Story 2 - Task Listing and Querying (Priority: P2)

**Goal**: Users can ask the AI to show their tasks using natural language queries

**Independent Test**: User can ask "What are my incomplete tasks?" or "Show me tasks about the project" and receive a formatted list of matching tasks

### Implementation for User Story 2

- [ ] T035 [US2] Enhance list_tasks MCP tool to support filtering by completion status in backend/ai_agent/tools/list_tasks.py
- [ ] T036 [US2] Add keyword search capability to list_tasks MCP tool in backend/ai_agent/tools/list_tasks.py
- [ ] T037 [US2] Update OpenSDK agent prompts to handle task listing queries in backend/ai_agent/agent.py
- [ ] T038 [US2] Format task lists in AI responses for readability in backend/ai_agent/agent.py
- [ ] T039 [US2] Handle empty task list responses gracefully in backend/ai_agent/agent.py

**Checkpoint**: At this point, User Story 2 should be fully functional - users can query and list tasks via chat

---

## Phase 6: User Story 3 - Task Completion via Chat (Priority: P3)

**Goal**: Users can mark tasks as complete or incomplete by telling the AI in natural language

**Independent Test**: User can say "Mark 'buy groceries' as done" and see the task's completion status update in both the chat and the task list UI

### Implementation for User Story 3

- [ ] T040 [P] [US3] Create complete_task MCP tool in backend/ai_agent/tools/complete_task.py
- [ ] T041 [US3] Register complete_task tool with OpenSDK agent in backend/ai_agent/agent.py
- [ ] T042 [US3] Update agent prompts to handle task completion requests in backend/ai_agent/agent.py
- [ ] T043 [US3] Implement task ambiguity resolution (multiple matches) in backend/ai_agent/agent.py
- [ ] T044 [US3] Handle non-existent task errors gracefully in backend/ai_agent/agent.py

**Checkpoint**: At this point, User Story 3 should be fully functional - users can complete/uncomplete tasks via chat

---

## Phase 7: User Story 4 - Task Updates via Chat (Priority: P4)

**Goal**: Users can update task details (title, description) by describing the changes to the AI in natural language

**Independent Test**: User can say "Change the title of my dentist task to 'Schedule dentist appointment'" and see the task title update in the task list

### Implementation for User Story 4

- [ ] T045 [P] [US4] Create update_task MCP tool in backend/ai_agent/tools/update_task.py
- [ ] T046 [US4] Register update_task tool with OpenSDK agent in backend/ai_agent/agent.py
- [ ] T047 [US4] Update agent prompts to handle task update requests in backend/ai_agent/agent.py
- [ ] T048 [US4] Implement partial update logic (title only, description only, or both) in backend/ai_agent/tools/update_task.py
- [ ] T049 [US4] Handle task ambiguity and non-existent task errors in backend/ai_agent/agent.py

**Checkpoint**: At this point, User Story 4 should be fully functional - users can update task details via chat

---

## Phase 8: User Story 7 - Conversation History (Priority: P4)

**Goal**: Users can view their previous conversations with the AI, allowing them to reference past interactions

**Independent Test**: User can access a list of past conversations, select one, and see the full message history from that conversation

### Implementation for User Story 7

- [ ] T050 [P] [US7] Create GET /api/{user_id}/conversations endpoint in backend/src/api/conversations.py
- [ ] T051 [P] [US7] Create GET /api/{user_id}/conversations/{id}/messages endpoint in backend/src/api/conversations.py
- [ ] T052 [P] [US7] Create ConversationList component in frontend/src/components/ConversationList.tsx
- [ ] T053 [US7] Implement conversation list fetching in useChat hook in frontend/src/hooks/useChat.ts
- [ ] T054 [US7] Implement conversation switching in useChat hook in frontend/src/hooks/useChat.ts
- [ ] T055 [US7] Add ConversationList to ChatInterface sidebar in frontend/src/components/ChatInterface.tsx
- [ ] T056 [US7] Implement message history loading on conversation switch in frontend/src/hooks/useChat.ts
- [ ] T057 [US7] Display conversation list ordered by most recent activity in frontend/src/components/ConversationList.tsx

**Checkpoint**: At this point, User Story 7 should be fully functional - users can view and switch between past conversations

---

## Phase 9: User Story 5 - Task Deletion via Chat (Priority: P5)

**Goal**: Users can delete tasks by asking the AI to remove them, with confirmation to prevent accidental deletion

**Independent Test**: User can say "Delete my grocery task" and after confirming, see the task removed from the task list

### Implementation for User Story 5

- [ ] T058 [P] [US5] Create delete_task MCP tool in backend/ai_agent/tools/delete_task.py
- [ ] T059 [US5] Register delete_task tool with OpenSDK agent in backend/ai_agent/agent.py
- [ ] T060 [US5] Implement deletion confirmation flow in backend/ai_agent/agent.py
- [ ] T061 [US5] Handle confirmation responses (yes/no/cancel) in backend/ai_agent/agent.py
- [ ] T062 [US5] Handle task ambiguity and non-existent task errors in backend/ai_agent/agent.py

**Checkpoint**: At this point, User Story 5 should be fully functional - users can delete tasks via chat with confirmation

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T063 [P] Add error handling for OpenRouter API failures in backend/ai_agent/agent.py
- [ ] T064 [P] Add error handling for Phase 2 API failures in all MCP tools in backend/ai_agent/tools/
- [ ] T065 [P] Implement retry logic with exponential backoff for OpenRouter API in backend/ai_agent/agent.py
- [ ] T066 [P] Add loading indicators in ChatInterface during AI processing in frontend/src/components/ChatInterface.tsx
- [ ] T067 [P] Add error message display in ChatInterface in frontend/src/components/ChatInterface.tsx
- [ ] T068 [P] Implement JWT token expiration handling in frontend/src/hooks/useChat.ts
- [ ] T069 [P] Add input sanitization for user messages in backend/src/api/conversations.py
- [ ] T070 [P] Implement conversation context loading (last 20 messages) in backend/ai_agent/agent.py
- [ ] T071 [P] Add logging for AI agent operations in backend/ai_agent/agent.py
- [ ] T072 [P] Add logging for MCP tool executions in backend/ai_agent/tools/
- [ ] T073 Verify Phase 2 functionality unchanged (manual testing)
- [ ] T074 Verify chat and task list synchronization (manual testing)
- [ ] T075 Test responsive design on mobile, tablet, desktop (manual testing)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 6 (Phase 3)**: Depends on Foundational phase completion
- **User Story 1 (Phase 4)**: Depends on Foundational phase completion
- **User Story 2 (Phase 5)**: Depends on User Story 1 completion (uses same MCP tools)
- **User Story 3 (Phase 6)**: Depends on User Story 1 completion (uses same agent infrastructure)
- **User Story 4 (Phase 7)**: Depends on User Story 1 completion (uses same agent infrastructure)
- **User Story 7 (Phase 8)**: Depends on User Story 6 completion (uses chat interface)
- **User Story 5 (Phase 9)**: Depends on User Story 1 completion (uses same agent infrastructure)
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 6 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on User Story 1 (uses list_tasks tool)
- **User Story 3 (P3)**: Depends on User Story 1 (uses agent infrastructure)
- **User Story 4 (P4)**: Depends on User Story 1 (uses agent infrastructure)
- **User Story 7 (P4)**: Depends on User Story 6 (uses chat interface)
- **User Story 5 (P5)**: Depends on User Story 1 (uses agent infrastructure)

### Within Each User Story

- Database models before services
- Services before API endpoints
- API endpoints before frontend components
- Frontend components before integration
- Core implementation before error handling

### Parallel Opportunities

- All Setup tasks (T001-T004) can run in parallel
- All Foundational model tasks (T007-T012) can run in parallel
- All Foundational MCP tool setup tasks (T014-T015) can run in parallel
- User Story 6 frontend components (T016-T019) can run in parallel
- User Story 1 MCP tools (T023-T025) can run in parallel
- User Story 7 API endpoints (T050-T051) and frontend components (T052) can run in parallel
- All Polish tasks (T063-T072) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all MCP tools for User Story 1 together:
Task: "Create list_tasks MCP tool in backend/ai_agent/tools/list_tasks.py"
Task: "Create create_task MCP tool in backend/ai_agent/tools/create_task.py"
Task: "Create get_task MCP tool in backend/ai_agent/tools/get_task.py"

# After tools complete, launch agent setup:
Task: "Initialize OpenSDK agent with OpenRouter in backend/ai_agent/agent.py"
```

---

## Implementation Strategy

### MVP First (User Stories 6 + 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 6 (Chat Interface Access)
4. Complete Phase 4: User Story 1 (Conversational Task Creation)
5. **STOP and VALIDATE**: Test User Stories 6 + 1 independently
6. Deploy/demo if ready

**MVP Delivers**: Users can open chat, create tasks via natural language, and see tasks in the list

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 6 → Test independently → Deploy/Demo (Chat UI works!)
3. Add User Story 1 → Test independently → Deploy/Demo (MVP! Task creation via chat)
4. Add User Story 2 → Test independently → Deploy/Demo (Task querying)
5. Add User Story 3 → Test independently → Deploy/Demo (Task completion)
6. Add User Story 4 → Test independently → Deploy/Demo (Task updates)
7. Add User Story 7 → Test independently → Deploy/Demo (Conversation history)
8. Add User Story 5 → Test independently → Deploy/Demo (Task deletion with confirmation)
9. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 6 (Chat Interface)
   - Developer B: User Story 1 (Task Creation)
3. After US1 complete:
   - Developer A: User Story 2 (Task Listing)
   - Developer B: User Story 3 (Task Completion)
   - Developer C: User Story 7 (Conversation History)
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Tests are OPTIONAL - not included as they were not explicitly requested in the specification

---

## Task Summary

**Total Tasks**: 75
- Setup: 4 tasks
- Foundational: 11 tasks
- User Story 6 (P1): 7 tasks
- User Story 1 (P1): 12 tasks
- User Story 2 (P2): 5 tasks
- User Story 3 (P3): 5 tasks
- User Story 4 (P4): 5 tasks
- User Story 7 (P4): 8 tasks
- User Story 5 (P5): 5 tasks
- Polish: 13 tasks

**Parallel Opportunities**: 28 tasks marked with [P] can run in parallel

**MVP Scope**: User Stories 6 + 1 (19 tasks after Setup + Foundational)

**Independent Test Criteria**:
- US6: Chat interface opens/closes without affecting Phase 2
- US1: Create task via chat, see in task list
- US2: Query tasks via chat, receive formatted list
- US3: Complete task via chat, see status update
- US4: Update task via chat, see changes in task list
- US7: View conversation history, switch between conversations
- US5: Delete task via chat with confirmation

**Format Validation**: ✅ All tasks follow checklist format with checkbox, ID, optional [P] and [Story] labels, and file paths
