---
description: "Task list for The Evolution of Todo – Phase I: In-Memory Python Console Application"
---

# Tasks: The Evolution of Todo – Phase I: In-Memory Python Console Application

**Input**: Design documents from `/specs/1-todo-cli-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks included as requested in feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 [P] Create directory structure: src/, src/todo/, tests/
- [X] T003 [P] Create __init__.py files in src/ and src/todo/
- [X] T004 [P] Initialize uv project with Python 3.11

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create Task model in src/todo/models.py
- [X] T006 [P] Create in-memory storage in src/todo/models.py
- [X] T007 Create TaskService in src/todo/service.py
- [X] T008 Create CLI interface foundation in src/todo/cli.py
- [X] T009 Create main application entry point in src/main.py
- [X] T010 Create basic test infrastructure in tests/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---
## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Allow users to add new tasks with required title and optional description

**Independent Test**: User can add a task with a title and optional description via the CLI, and the task appears in the system with a unique ID and completion status of incomplete.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T011 [P] [US1] Create Task model tests in tests/test_models.py
- [X] T012 [P] [US1] Create add task service test in tests/test_service.py
- [X] T013 [P] [US1] Create add task CLI test in tests/test_cli.py

### Implementation for User Story 1

- [X] T014 [US1] Implement Task class with id, title, description, completed in src/todo/models.py
- [X] T015 [US1] Implement TaskService.add_task() method in src/todo/service.py
- [X] T016 [US1] Implement add command in CLI interface in src/todo/cli.py
- [X] T017 [US1] Add add command to main application in src/main.py
- [X] T018 [US1] Add validation for required title field in src/todo/service.py

**Checkpoint**: At this point, users should be able to add tasks via CLI and see them stored in memory

---
## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Allow users to view all tasks with their ID, title, and completion status

**Independent Test**: User can view all tasks with their ID, title, and completion status in a clear format.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T019 [P] [US2] Create list tasks service test in tests/test_service.py
- [X] T020 [P] [US2] Create list tasks CLI test in tests/test_cli.py

### Implementation for User Story 2

- [X] T021 [US2] Implement TaskService.list_tasks() method in src/todo/service.py
- [X] T022 [US2] Implement list command in CLI interface in src/todo/cli.py
- [X] T023 [US2] Add list command to main application in src/main.py
- [X] T024 [US2] Format task display with ID, title, and completion status (✓/✗) in src/todo/cli.py

**Checkpoint**: At this point, users should be able to add and view tasks

---
## Phase 5: User Story 5 - Mark Tasks Complete/Incomplete (Priority: P1)

**Goal**: Allow users to mark tasks as complete or incomplete by ID

**Independent Test**: User can toggle the completion status of a task by specifying the task ID.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [X] T025 [P] [US5] Create mark complete service test in tests/test_service.py
- [X] T026 [P] [US5] Create mark incomplete service test in tests/test_service.py
- [X] T027 [P] [US5] Create complete command CLI test in tests/test_cli.py
- [X] T028 [P] [US5] Create incomplete command CLI test in tests/test_cli.py

### Implementation for User Story 5

- [X] T029 [US5] Implement TaskService.mark_task_complete() method in src/todo/service.py
- [X] T030 [US5] Implement TaskService.mark_task_incomplete() method in src/todo/service.py
- [X] T031 [US5] Implement complete command in CLI interface in src/todo/cli.py
- [X] T032 [US5] Implement incomplete command in CLI interface in src/todo/cli.py
- [X] T033 [US5] Add complete command to main application in src/main.py
- [X] T034 [US5] Add incomplete command to main application in src/main.py

**Checkpoint**: At this point, users should be able to add, view, and mark tasks complete/incomplete

---
## Phase 6: User Story 3 - Update Existing Tasks (Priority: P2)

**Goal**: Allow users to update existing tasks' title and/or description by ID

**Independent Test**: User can update a task's title and/or description by specifying the task ID.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T035 [P] [US3] Create update task service test in tests/test_service.py
- [X] T036 [P] [US3] Create update task CLI test in tests/test_cli.py

### Implementation for User Story 3

- [X] T037 [US3] Implement TaskService.update_task() method in src/todo/service.py
- [X] T038 [US3] Implement update command in CLI interface in src/todo/cli.py
- [X] T039 [US3] Add update command to main application in src/main.py

**Checkpoint**: At this point, users should be able to add, view, update, and mark tasks complete/incomplete

---
## Phase 7: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Allow users to delete tasks by ID

**Independent Test**: User can remove a task from the list by specifying the task ID.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T040 [P] [US4] Create delete task service test in tests/test_service.py
- [X] T041 [P] [US4] Create delete task CLI test in tests/test_cli.py

### Implementation for User Story 4

- [X] T042 [US4] Implement TaskService.delete_task() method in src/todo/service.py
- [X] T043 [US4] Implement delete command in CLI interface in src/todo/cli.py
- [X] T044 [US4] Add delete command to main application in src/main.py

**Checkpoint**: All user stories should now be independently functional

---
## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T045 [P] Add comprehensive error handling for all operations in src/todo/service.py
- [X] T046 [P] Add input validation for all commands in src/todo/cli.py
- [X] T047 [P] Add proper error messages for invalid task IDs in src/todo/service.py
- [X] T048 [P] Add help text and documentation for all commands in src/todo/cli.py
- [X] T049 [P] Add unit tests for error conditions in tests/test_service.py
- [X] T050 Run integration tests to ensure all functionality works together

---
## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services (completed in foundational phase)
- Services before CLI commands
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---
## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Create Task model tests in tests/test_models.py"
Task: "Create add task service test in tests/test_service.py"
Task: "Create add task CLI test in tests/test_cli.py"

# Launch all implementation for User Story 1 together:
Task: "Implement Task class with id, title, description, completed in src/todo/models.py"
Task: "Implement TaskService.add_task() method in src/todo/service.py"
Task: "Implement add command in CLI interface in src/todo/cli.py"
```

---
## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Tasks)
4. **STOP and VALIDATE**: Test adding tasks independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 5 → Test independently → Deploy/Demo
5. Add User Story 3 → Test independently → Deploy/Demo
6. Add User Story 4 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Add Tasks)
   - Developer B: User Story 2 (View Tasks)
   - Developer C: User Story 5 (Complete/Incomplete)
   - Developer D: User Story 3 (Update) and User Story 4 (Delete)
3. Stories complete and integrate independently

---
## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence