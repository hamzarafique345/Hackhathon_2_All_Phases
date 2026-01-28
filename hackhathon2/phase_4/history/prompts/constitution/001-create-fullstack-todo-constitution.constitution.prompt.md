---
id: 001
title: Create Full-Stack Todo App Constitution
stage: constitution
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-todo-fullstack-web
user: hamzarafique345
command: /sp.constitution
labels: ["constitution", "setup", "governance", "security", "workflow"]
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

Create CONSTITUTION.md for a full-stack todo app with these rules:

PROJECT SETUP:
- Frontend: Next.js 16 (App Router) - already installed in /frontend
- Backend: Python FastAPI - empty /backend folder
- Database: Neon PostgreSQL
- Auth: Better Auth with JWT tokens

WORKFLOW (Mandatory):
1. Write spec first (no coding without spec)
2. Generate plan from spec
3. Break plan into tasks
4. Execute via Claude Code only (zero manual coding)

TECHNOLOGY STACK:
Frontend: Next.js 16, TypeScript, TailwindCSS, Better Auth (JWT), shadcn/ui, Axios
Backend: FastAPI, SQLModel, PyJWT, bcrypt, python-dotenv

API ENDPOINTS (Required):
- GET /api/{user_id}/tasks - List tasks
- POST /api/{user_id}/tasks - Create task
- GET /api/{user_id}/tasks/{id} - Get task
- PUT /api/{user_id}/tasks/{id} - Update task
- DELETE /api/{user_id}/tasks/{id} - Delete task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle complete

SECURITY (Non-Negotiable):
- All API calls include JWT in Authorization: Bearer {token}
- Backend verifies JWT on every endpoint
- URL user_id must match JWT user_id (else 403)
- Users can ONLY access their own data
- Same BETTER_AUTH_SECRET in frontend and backend

DATABASE SCHEMA:
users: id (uuid), email (unique), password_hash, name, created_at
tasks: id (uuid), user_id (fk), title, description, completed (bool), created_at

UI REQUIREMENTS:
- Landing page: Modern hero section, features grid, CTA buttons
- Auth pages: Centered card layout, inline validation, loading states
- Responsive: Mobile-first design
- Colors: Blue-purple gradient, clean typography

QUALITY GATES:
- JWT authentication working
- User isolation enforced (test with 2 users)
- Forms validated (client + server)
- Responsive on mobile/tablet/desktop
- No secrets in code (use .env files)

ENV VARIABLES:
Frontend: BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_API_URL
Backend: DATABASE_URL, BETTER_AUTH_SECRET, JWT_ALGORITHM

Generate constitution with sections: Overview, Workflow, Tech Stack, API Contract, Security, Database, UI Standards, Quality Gates.

## Response snapshot

Created comprehensive constitution v1.0.0 at `.specify/memory/constitution.md` with the following structure:

**Core Principles (6 NON-NEGOTIABLE rules)**:
1. Spec-First Development - Mandatory workflow: Spec → Plan → Tasks → Execution
2. Security-First Architecture - JWT authentication, user isolation, secret management
3. Full-Stack Type Safety - TypeScript (frontend), Python type hints (backend)
4. Environment-Based Configuration - .env files for all secrets
5. Responsive Design (Mobile-First) - Mobile < 768px, Tablet 768-1024px, Desktop > 1024px
6. API Contract Compliance - 6 required endpoints with exact paths

**Additional Sections**:
- Development Workflow (5 phases: Specification → Planning → Task Breakdown → Execution → Validation)
- Technology Stack (Frontend: Next.js 16/TypeScript/TailwindCSS, Backend: FastAPI/SQLModel/PyJWT)
- API Contract (Authentication flow, request/response formats, status codes)
- Security Requirements (Authentication, authorization, transport, input validation, secrets)
- Database Schema (Users and Tasks tables with constraints and indexes)
- UI Standards (Landing page, auth pages, dashboard, forms, responsive breakpoints, color scheme)
- Quality Gates (6 gates: Authentication, Authorization, Validation, Responsive, Security, Functional)
- Governance (Amendment process, versioning policy, compliance review, enforcement)

**Sync Impact Report**:
- Version: 1.0.0 (initial creation)
- Ratified: 2026-01-08
- Templates verified: spec-template.md, plan-template.md, tasks-template.md (all aligned)
- No follow-up TODOs

## Outcome

- ✅ Impact: Constitution v1.0.0 created with 6 core principles, comprehensive security requirements, and 6 quality gates
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: 1 file created (.specify/memory/constitution.md - 479 lines)
- 🔁 Next prompts: Run `/sp.specify` to create first feature specification following the mandatory workflow
- 🧠 Reflection: Constitution establishes strong security foundation with JWT authentication, user isolation, and environment-based configuration. Mobile-first responsive design and spec-driven workflow ensure quality and consistency.

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution created successfully with all required sections
- Graders run and results (PASS/FAIL): PASS - All placeholders filled, no unresolved tokens, version semantics correct
- Prompt variant (if applicable): N/A (initial constitution creation)
- Next experiment (smallest change to try): Test workflow by creating first feature spec using `/sp.specify` command
