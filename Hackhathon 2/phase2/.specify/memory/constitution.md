<!--
SYNC IMPACT REPORT
==================
Version Change: INITIAL → 1.0.0
Created: 2026-01-08
Type: Initial constitution creation

Sections Added:
- Overview
- Core Principles (6 principles)
- Development Workflow
- Technology Stack
- API Contract
- Security Requirements
- Database Schema
- UI Standards
- Quality Gates
- Governance

Templates Status:
✅ spec-template.md - Aligned (user stories support independent testing)
✅ plan-template.md - Aligned (constitution check section ready)
✅ tasks-template.md - Aligned (phase-based structure matches workflow)

Follow-up TODOs: None
-->

# Full-Stack Todo App Constitution

## Overview

This constitution governs the development of a full-stack todo application built with Next.js 16 (frontend) and Python FastAPI (backend), using Neon PostgreSQL for data persistence and Better Auth with JWT tokens for authentication.

**Project Structure**:
- `/frontend` - Next.js 16 application (App Router)
- `/backend` - Python FastAPI application
- Database: Neon PostgreSQL (cloud-hosted)

**Development Philosophy**: Spec-driven development with zero manual coding. All implementation work must flow through Claude Code following the mandatory workflow: Spec → Plan → Tasks → Execution.

## Core Principles

### I. Spec-First Development (NON-NEGOTIABLE)

**Rule**: No code may be written without an approved specification.

**Workflow Enforcement**:
1. Write feature specification using `/sp.specify`
2. Generate implementation plan using `/sp.plan`
3. Break plan into tasks using `/sp.tasks`
4. Execute tasks via Claude Code only (zero manual coding allowed)

**Rationale**: Prevents scope creep, ensures architectural consistency, and maintains traceability from requirements to implementation.

### II. Security-First Architecture (NON-NEGOTIABLE)

**Authentication Requirements**:
- All API endpoints MUST verify JWT tokens on every request
- JWT tokens MUST be included in `Authorization: Bearer {token}` header
- Backend MUST validate token signature using shared `BETTER_AUTH_SECRET`

**Authorization Requirements**:
- URL `user_id` parameter MUST match JWT `user_id` claim
- Mismatch MUST return HTTP 403 Forbidden
- Users MUST ONLY access their own data (strict user isolation)

**Secret Management**:
- NEVER commit secrets to version control
- ALL secrets MUST be in `.env` files (gitignored)
- Frontend and backend MUST share identical `BETTER_AUTH_SECRET`

**Rationale**: Security vulnerabilities are unacceptable. User data isolation is a legal and ethical requirement.

### III. Full-Stack Type Safety

**Frontend Requirements**:
- TypeScript MUST be used for all code
- Strict mode MUST be enabled in `tsconfig.json`
- API response types MUST be defined and validated

**Backend Requirements**:
- Python type hints MUST be used for all functions
- SQLModel MUST be used for database models (provides Pydantic validation)
- FastAPI automatic validation MUST be leveraged

**Rationale**: Type safety catches bugs at compile time, improves IDE support, and serves as living documentation.

### IV. Environment-Based Configuration

**Required Environment Variables**:

Frontend (`.env.local`):
- `BETTER_AUTH_SECRET` - Shared secret for JWT signing/verification
- `BETTER_AUTH_URL` - Base URL for auth endpoints
- `NEXT_PUBLIC_API_URL` - Backend API base URL

Backend (`.env`):
- `DATABASE_URL` - Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET` - Shared secret (MUST match frontend)
- `JWT_ALGORITHM` - Algorithm for JWT (default: HS256)

**Rules**:
- `.env` files MUST be in `.gitignore`
- `.env.example` files MUST be provided with placeholder values
- Application MUST fail fast on startup if required variables are missing

**Rationale**: Separates configuration from code, enables environment-specific deployments, prevents secret leakage.

### V. Responsive Design (Mobile-First)

**Design Requirements**:
- Mobile breakpoint (< 768px) designed first
- Tablet breakpoint (768px - 1024px) tested
- Desktop breakpoint (> 1024px) tested
- Touch targets MUST be minimum 44x44px
- Text MUST be readable without zooming (minimum 16px base)

**UI Component Standards**:
- Use shadcn/ui components for consistency
- TailwindCSS utility classes for styling
- Blue-purple gradient color scheme
- Clean, modern typography (system fonts)

**Rationale**: Mobile traffic dominates web usage. Mobile-first ensures usability on all devices.

### VI. API Contract Compliance (NON-NEGOTIABLE)

**Required Endpoints** (all under `/api/{user_id}/tasks`):

```
GET    /api/{user_id}/tasks           - List all tasks for user
POST   /api/{user_id}/tasks           - Create new task
GET    /api/{user_id}/tasks/{id}      - Get single task
PUT    /api/{user_id}/tasks/{id}      - Update task (full replacement)
DELETE /api/{user_id}/tasks/{id}      - Delete task
PATCH  /api/{user_id}/tasks/{id}/complete - Toggle completion status
```

**Contract Rules**:
- Endpoint paths MUST match exactly as specified
- All endpoints MUST require JWT authentication
- All endpoints MUST validate `user_id` matches JWT claim
- Response format MUST be consistent JSON
- Error responses MUST include meaningful messages

**Rationale**: API contract is the interface between frontend and backend. Breaking changes cause integration failures.

## Development Workflow

### Phase 1: Specification
- Run `/sp.specify` with feature description
- Review generated `spec.md` for completeness
- Clarify ambiguities before proceeding
- Approval required before moving to planning

### Phase 2: Planning
- Run `/sp.plan` to generate implementation plan
- Review `plan.md`, `research.md`, `data-model.md`, `contracts/`
- Validate against constitution principles
- Approval required before task generation

### Phase 3: Task Breakdown
- Run `/sp.tasks` to generate task list
- Review `tasks.md` for completeness and ordering
- Ensure tasks are atomic and testable
- Approval required before execution

### Phase 4: Execution
- Execute tasks via Claude Code only
- No manual coding allowed
- Commit after each logical task group
- Test continuously during implementation

### Phase 5: Validation
- Run all quality gates (see Quality Gates section)
- Fix any failures before considering feature complete
- Document any deviations in ADR

## Technology Stack

### Frontend Stack
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: TailwindCSS
- **UI Components**: shadcn/ui
- **Authentication**: Better Auth (JWT mode)
- **HTTP Client**: Axios
- **State Management**: React hooks (useState, useContext)

### Backend Stack
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Authentication**: PyJWT for token verification
- **Password Hashing**: bcrypt
- **Environment**: python-dotenv
- **Database Driver**: asyncpg (for PostgreSQL)

### Database
- **Provider**: Neon PostgreSQL (serverless)
- **Connection**: Pooled connections via asyncpg
- **Migrations**: Alembic (SQLAlchemy migrations)

### Development Tools
- **Version Control**: Git
- **Package Managers**: npm (frontend), pip (backend)
- **Code Quality**: ESLint (frontend), Ruff (backend)
- **Type Checking**: TypeScript compiler, mypy (backend)

## API Contract

### Authentication Flow
1. User registers/logs in via Better Auth
2. Better Auth returns JWT token
3. Frontend stores token (httpOnly cookie or localStorage)
4. Frontend includes token in all API requests: `Authorization: Bearer {token}`
5. Backend validates token and extracts `user_id` claim
6. Backend verifies URL `user_id` matches token `user_id`

### Request Format

**Create Task**:
```json
POST /api/{user_id}/tasks
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "title": "Task title",
  "description": "Task description"
}
```

**Update Task**:
```json
PUT /api/{user_id}/tasks/{task_id}
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "completed": false
}
```

### Response Format

**Success Response**:
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "created_at": "2026-01-08T12:00:00Z"
}
```

**Error Response**:
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Status Codes
- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Missing or invalid JWT token
- `403 Forbidden` - User attempting to access another user's data
- `404 Not Found` - Resource does not exist
- `500 Internal Server Error` - Server-side error

## Security Requirements

### Authentication Security
- JWT tokens MUST expire (recommended: 24 hours)
- Refresh token mechanism SHOULD be implemented for long sessions
- Password MUST be hashed with bcrypt (minimum 12 rounds)
- NEVER store plain-text passwords

### Authorization Security
- EVERY endpoint MUST validate JWT token
- EVERY endpoint MUST verify `user_id` in URL matches JWT claim
- Database queries MUST filter by `user_id` to prevent data leakage
- SQL injection MUST be prevented (use parameterized queries via SQLModel)

### Transport Security
- Production MUST use HTTPS only
- Development MAY use HTTP for localhost
- CORS MUST be configured to allow only trusted origins

### Input Validation
- Frontend MUST validate all form inputs before submission
- Backend MUST validate all inputs (never trust client)
- Sanitize inputs to prevent XSS attacks
- Limit input lengths to prevent DoS

### Secret Management
- Secrets MUST be in `.env` files
- `.env` files MUST be in `.gitignore`
- Provide `.env.example` with placeholder values
- Rotate secrets periodically in production

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Constraints**:
- `email` MUST be unique
- `email` MUST be validated format
- `password_hash` MUST be bcrypt hash (never plain text)

### Tasks Table
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Constraints**:
- `user_id` MUST reference valid user (foreign key)
- `title` MUST NOT be empty
- `completed` defaults to `false`
- Deleting user MUST cascade delete all their tasks

**Indexes**:
- Index on `user_id` for fast task lookups per user
- Index on `created_at` for chronological sorting

## UI Standards

### Landing Page
- Hero section with compelling headline and subheadline
- Features grid (3-4 key features with icons)
- Call-to-action buttons (Sign Up, Log In)
- Responsive layout (stacks vertically on mobile)
- Blue-purple gradient background or accents

### Authentication Pages
- Centered card layout (max-width 400px)
- Form fields with labels and placeholders
- Inline validation (show errors below fields)
- Loading states during submission (disable button, show spinner)
- Success/error messages displayed prominently
- Link to alternate auth page (Login ↔ Register)

### Dashboard/Tasks Page
- Header with user name and logout button
- Task list with checkboxes for completion
- Add task button (prominent, easy to find)
- Each task shows title, description, completion status
- Edit and delete buttons per task
- Empty state when no tasks ("Get started by adding your first task")

### Forms
- Required fields marked with asterisk (*)
- Validation on blur and on submit
- Error messages in red below field
- Success messages in green
- Disabled submit button while loading

### Responsive Breakpoints
- Mobile: < 768px (single column, full width)
- Tablet: 768px - 1024px (may use 2 columns for task grid)
- Desktop: > 1024px (max content width 1200px, centered)

### Color Scheme
- Primary: Blue (#3B82F6) to Purple (#8B5CF6) gradient
- Success: Green (#10B981)
- Error: Red (#EF4444)
- Text: Gray-900 (#111827) on light backgrounds
- Background: White (#FFFFFF) or Gray-50 (#F9FAFB)

### Typography
- Font: System font stack (sans-serif)
- Base size: 16px
- Headings: Bold, larger sizes (h1: 2.5rem, h2: 2rem, h3: 1.5rem)
- Body: Regular weight, 1.5 line height

## Quality Gates

All features MUST pass these gates before being considered complete:

### 1. Authentication Gate
- [ ] User can register with email and password
- [ ] User can log in with valid credentials
- [ ] Invalid credentials are rejected with clear error
- [ ] JWT token is returned on successful login
- [ ] Token is stored and included in subsequent API requests

### 2. Authorization Gate
- [ ] Create two test users (User A, User B)
- [ ] User A can create tasks and see only their tasks
- [ ] User B can create tasks and see only their tasks
- [ ] User A CANNOT access User B's tasks (403 error)
- [ ] User B CANNOT access User A's tasks (403 error)
- [ ] Direct API calls with mismatched user_id are rejected

### 3. Validation Gate
- [ ] Frontend validates required fields before submission
- [ ] Backend validates all inputs (duplicate frontend validation)
- [ ] Empty task title is rejected
- [ ] Invalid email format is rejected during registration
- [ ] Weak passwords are rejected (minimum 8 characters)
- [ ] Error messages are clear and actionable

### 4. Responsive Gate
- [ ] Test on mobile viewport (375px width)
- [ ] Test on tablet viewport (768px width)
- [ ] Test on desktop viewport (1440px width)
- [ ] All text is readable without zooming
- [ ] All buttons are tappable (minimum 44x44px)
- [ ] Layout does not break or overflow

### 5. Security Gate
- [ ] No secrets in committed code (check git history)
- [ ] `.env` files are in `.gitignore`
- [ ] `.env.example` files provided with placeholders
- [ ] All API endpoints verify JWT token
- [ ] All API endpoints verify user_id authorization
- [ ] Passwords are hashed (never stored plain text)

### 6. Functional Gate
- [ ] All 6 API endpoints work correctly
- [ ] Tasks can be created, read, updated, deleted
- [ ] Task completion can be toggled
- [ ] Task list updates in real-time after operations
- [ ] Error handling works (network errors, server errors)

## Governance

### Constitution Authority
This constitution supersedes all other development practices and preferences. When conflicts arise between this constitution and other guidance, the constitution takes precedence.

### Amendment Process
1. Propose amendment with clear rationale
2. Document impact on existing code and templates
3. Update constitution version (semantic versioning)
4. Update all dependent templates and documentation
5. Create ADR documenting the decision
6. Commit with message: `docs: amend constitution to vX.Y.Z (description)`

### Versioning Policy
- **MAJOR** (X.0.0): Backward-incompatible changes (principle removal, redefinition)
- **MINOR** (0.X.0): New principles or sections added
- **PATCH** (0.0.X): Clarifications, typo fixes, non-semantic changes

### Compliance Review
- All specifications MUST reference constitution principles
- All plans MUST include "Constitution Check" section
- All pull requests MUST verify compliance
- Violations MUST be justified in ADR or rejected

### Enforcement
- Claude Code MUST validate against constitution during execution
- Automated checks SHOULD be added where possible
- Manual review REQUIRED for principle violations
- Zero tolerance for security principle violations

**Version**: 1.0.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08
