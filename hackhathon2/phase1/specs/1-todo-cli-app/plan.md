# Implementation Plan: The Evolution of Todo – Phase I: In-Memory Python Console Application

**Branch**: `1-todo-cli-app` | **Date**: 2026-01-02 | **Spec**: [link]
**Input**: Feature specification from `/specs/history/phase-1-spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Python 3.11 CLI-based todo application with in-memory storage. The application will support all required functionality: adding, viewing, updating, deleting, and marking tasks complete/incomplete. The design follows clean architecture principles with separation of concerns between models, services, and CLI interface.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: Standard library only (as per constitution)
**Storage**: In-memory only, no persistence
**Testing**: unittest module (standard library)
**Target Platform**: Cross-platform CLI application
**Project Type**: Single console application
**Performance Goals**: Fast response times for CLI operations (under 1 second)
**Constraints**: <200ms for basic operations, <100MB memory usage for normal operation
**Scale/Scope**: Single-user, local application

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Spec-Driven Development ONLY: Following plan after specification approval
- ✅ No Manual Coding by User: AI agent will generate all code
- ✅ Clean Architecture & Clean Code: Designing with separation of concerns
- ✅ Python Project Standards: Using Python 3.11, in-memory storage, CLI-only
- ✅ Folder Structure Rules: Using /src for source code
- ✅ Tooling Requirements: Using uv for environment management
- ✅ Output Expectations: CLI-based application with no persistence beyond runtime

## Project Structure

### Documentation (this feature)
```
specs/1-todo-cli-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```
src/
├── main.py
├── todo/
│   ├── __init__.py
│   ├── models.py
│   ├── service.py
│   └── cli.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_service.py
    └── test_cli.py
```

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

## Phase 0: Research & Analysis

1. **Python CLI Framework Decision**
   - Decision: Use built-in `argparse` module
   - Rationale: Part of standard library, meets constitution requirements, sufficient for CLI needs
   - Alternatives considered: click library (requires external dependency), sys.argv (too basic)

2. **In-Memory Storage Approach**
   - Decision: Use Python dictionary with integer keys for task IDs
   - Rationale: Simple, efficient, fits in-memory requirement perfectly
   - Alternatives considered: List storage (less efficient for lookups by ID)

3. **Task ID Generation**
   - Decision: Use auto-incrementing integer IDs starting from 1
   - Rationale: Simple, efficient, easy for users to reference
   - Alternatives considered: UUIDs (too complex for CLI), random integers (risk of collisions)

## Phase 1: Data Model Design

### Task Entity Design
- **Task**: Core entity with the following attributes:
  - `id`: Integer, unique identifier (auto-generated)
  - `title`: String, required, non-empty
  - `description`: String, optional, can be None
  - `completed`: Boolean, default False

### Validation Rules
- Title must be provided and not empty when creating a task
- Task ID must exist for update/delete/complete operations
- All operations must handle non-existent task IDs gracefully

### State Transitions
- `incomplete` → `complete`: When marking task as done
- `complete` → `incomplete`: When marking task as not done

## Phase 2: API Contracts

### CLI Commands Design
1. `add` - Add a new task
   - Arguments: `--title` (required), `--description` (optional)
   - Returns: Success message with assigned task ID

2. `list` - View all tasks
   - Arguments: None
   - Returns: Formatted list of all tasks with ID, title, and completion status

3. `update` - Update an existing task
   - Arguments: `--id` (required), `--title` (optional), `--description` (optional)
   - Returns: Success message or error if task doesn't exist

4. `delete` - Delete a task
   - Arguments: `--id` (required)
   - Returns: Success message or error if task doesn't exist

5. `complete` - Mark task as complete
   - Arguments: `--id` (required)
   - Returns: Success message or error if task doesn't exist

6. `incomplete` - Mark task as incomplete
   - Arguments: `--id` (required)
   - Returns: Success message or error if task doesn't exist

## Phase 3: Implementation Approach

### Module Design
1. `models.py`: Defines the Task class and in-memory storage
2. `service.py`: Business logic for task operations
3. `cli.py`: Command-line interface using argparse
4. `main.py`: Application entry point that orchestrates the other modules

### Error Handling Strategy
- Input validation at CLI level
- Business logic validation in service layer
- Graceful error messages to user
- No system crashes on invalid inputs

### Execution Order
1. Initialize project with uv and Python 3.11
2. Create directory structure
3. Implement data models
4. Implement service layer
5. Implement CLI interface
6. Create main application entry point
7. Write unit tests
8. Create quickstart guide