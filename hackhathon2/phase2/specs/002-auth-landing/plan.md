# Implementation Plan: Authentication and Landing Page

**Branch**: `002-auth-landing` | **Date**: 2026-01-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-auth-landing/spec.md`

## Summary

This feature implements a complete authentication system with landing page for the full-stack todo application. The implementation includes a responsive landing page with hero section and feature cards, user registration and sign-in flows using Better Auth with JWT tokens, and protected dashboard access with automatic authentication verification. The system enforces strict security requirements including JWT validation on all protected endpoints, user data isolation, and secure secret management.

**Technical Approach**: Web application architecture with Next.js 16 (App Router) frontend and Python FastAPI backend, using Better Auth for JWT-based authentication and Neon PostgreSQL for data persistence. The frontend uses shadcn/ui components with TailwindCSS for responsive design, while the backend uses SQLModel for type-safe database operations and PyJWT for token verification.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x with Next.js 16 (App Router)
- Backend: Python 3.11+

**Primary Dependencies**:
- Frontend: Next.js 16, Better Auth (JWT plugin), Axios, shadcn/ui, TailwindCSS, Lucide React (icons)
- Backend: FastAPI, SQLModel, PyJWT, Passlib (bcrypt), python-dotenv, asyncpg

**Storage**: Neon PostgreSQL (serverless, cloud-hosted)

**Testing**:
- Frontend: Jest + React Testing Library (future phase)
- Backend: pytest (future phase)

**Target Platform**:
- Frontend: Web browsers (Chrome, Firefox, Safari, Edge - last 2 versions)
- Backend: Linux server (containerized deployment)

**Project Type**: Web application (frontend + backend)

**Performance Goals**:
- Landing page load time: <2 seconds
- Sign-up completion: <90 seconds end-to-end
- Sign-in completion: <30 seconds end-to-end
- API response time: <500ms for authentication endpoints

**Constraints**:
- JWT tokens must be validated on every protected endpoint request
- User data isolation enforced (user_id in URL must match JWT claim)
- No secrets in version control (all in .env files)
- Mobile-first responsive design (375px, 768px, 1440px breakpoints)

**Scale/Scope**:
- Initial deployment: 100-1000 concurrent users
- Database: 10,000+ user accounts
- Session duration: 7 days for "Remember me", session-based otherwise

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Spec-First Development ✅ PASS
- ✅ Specification created and approved (spec.md)
- ✅ Following mandatory workflow: Spec → Plan → Tasks → Execution
- ✅ No code written before planning phase

### II. Security-First Architecture ✅ PASS
- ✅ JWT authentication on all protected endpoints (FR-033)
- ✅ User data isolation enforced (user_id matching required)
- ✅ Secrets in .env files only (FR-040, constitution requirement)
- ✅ Shared BETTER_AUTH_SECRET between frontend and backend
- ✅ Password hashing with bcrypt (minimum 12 rounds, FR-040)

### III. Full-Stack Type Safety ✅ PASS
- ✅ TypeScript with strict mode for frontend
- ✅ Python type hints for all backend functions
- ✅ SQLModel for database models (Pydantic validation)
- ✅ FastAPI automatic request/response validation

### IV. Environment-Based Configuration ✅ PASS
- ✅ Frontend .env.local: BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_API_URL
- ✅ Backend .env: DATABASE_URL, BETTER_AUTH_SECRET, JWT_ALGORITHM
- ✅ .env files in .gitignore
- ✅ .env.example files to be provided

### V. Responsive Design (Mobile-First) ✅ PASS
- ✅ Mobile breakpoint (<768px) designed first
- ✅ Tablet (768px-1024px) and desktop (>1024px) tested
- ✅ Touch targets minimum 44x44px
- ✅ Base font size 16px minimum
- ✅ shadcn/ui components for consistency
- ✅ Blue-purple gradient color scheme

### VI. API Contract Compliance ✅ PASS
- ✅ Authentication endpoints defined (sign-up, sign-in)
- ✅ Health check endpoint (FR-038)
- ✅ JWT required for protected endpoints
- ✅ Consistent JSON response format
- ✅ Meaningful error messages

**Constitution Check Result**: ALL GATES PASSED - No violations, no complexity justification needed

## Project Structure

### Documentation (this feature)

```text
specs/002-auth-landing/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── auth-api.yaml    # Authentication endpoints
│   └── health-api.yaml  # Health check endpoint
├── checklists/
│   └── requirements.md  # Specification quality checklist
└── spec.md              # Feature specification
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models.py        # SQLModel User and Task models
│   ├── database.py      # Neon PostgreSQL connection
│   ├── auth.py          # JWT verification and dependencies
│   ├── main.py          # FastAPI app, CORS, routes
│   └── __init__.py
├── tests/               # Future phase
├── .env                 # Backend environment variables (gitignored)
├── .env.example         # Backend environment template
├── requirements.txt     # Python dependencies
└── README.md

frontend/
├── app/
│   ├── page.tsx         # Landing page (root)
│   ├── signup/
│   │   └── page.tsx     # Sign-up page
│   ├── signin/
│   │   └── page.tsx     # Sign-in page
│   ├── dashboard/
│   │   └── page.tsx     # Protected dashboard
│   └── layout.tsx       # Root layout
├── components/
│   ├── landing/
│   │   ├── Hero.tsx     # Hero section
│   │   ├── Features.tsx # Feature cards
│   │   └── CTA.tsx      # Call-to-action section
│   ├── auth/
│   │   ├── SignUpForm.tsx    # Sign-up form
│   │   ├── SignInForm.tsx    # Sign-in form
│   │   └── AuthContext.tsx   # Global auth state
│   └── ui/              # shadcn/ui components
│       ├── button.tsx
│       ├── input.tsx
│       ├── label.tsx
│       └── card.tsx
├── lib/
│   ├── auth.ts          # Better Auth configuration
│   └── api-client.ts    # Axios instance with JWT interceptor
├── .env.local           # Frontend environment variables (gitignored)
├── .env.example         # Frontend environment template
├── package.json
└── README.md
```

**Structure Decision**: Web application structure selected based on constitution requirements (frontend + backend). Frontend uses Next.js 16 App Router structure with app/ directory for pages and components/ for reusable UI. Backend uses FastAPI with src/ directory for Python modules. Both include .env files for environment-based configuration and .env.example templates for documentation.

## Complexity Tracking

> **No violations detected - this section is empty**

## Implementation Phases

### Phase 0: Research & Technology Validation ✅

**Purpose**: Validate technology choices and resolve any unknowns before design phase.

**Research Topics**:
1. Better Auth JWT plugin configuration for Next.js 16 App Router
2. FastAPI + SQLModel best practices for async PostgreSQL
3. Neon PostgreSQL connection pooling and configuration
4. shadcn/ui component installation and customization
5. JWT token storage strategies (httpOnly cookies vs localStorage)

**Output**: research.md with decisions, rationale, and alternatives considered

**Status**: To be completed in this command execution

---

### Phase 1: Design & Contracts ✅

**Purpose**: Define data models, API contracts, and quickstart guide.

**Deliverables**:
1. **data-model.md**: User and Task entity definitions with validation rules
2. **contracts/auth-api.yaml**: OpenAPI spec for authentication endpoints
3. **contracts/health-api.yaml**: OpenAPI spec for health check endpoint
4. **quickstart.md**: Setup instructions for local development

**Status**: To be completed in this command execution

---

### Phase 2: Environment Setup (Tasks Phase)

**Purpose**: Install dependencies and configure development environment.

**Tasks** (to be detailed in tasks.md):
- Install frontend dependencies (better-auth, axios, shadcn/ui, lucide-react)
- Install backend dependencies (fastapi, sqlmodel, pyjwt, passlib, psycopg2)
- Create .env.local with BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_API_URL
- Create .env with DATABASE_URL, BETTER_AUTH_SECRET, JWT_ALGORITHM
- Initialize Neon database and create tables

**Dependencies**: None (first phase)

**Verification**:
- `npm run dev` works for frontend
- `uvicorn main:app --reload` works for backend
- Database connection successful

**Estimated Duration**: 30-45 minutes

---

### Phase 3: Backend Foundation (Tasks Phase)

**Purpose**: Create core backend infrastructure for authentication.

**Tasks** (to be detailed in tasks.md):
- Create database.py with SQLModel engine and Neon connection
- Create models.py with User and Task SQLModel classes
- Create auth.py with verify_jwt_token() and get_current_user() dependency
- Create main.py with FastAPI app, CORS middleware, and health check endpoint
- Test database connection and JWT verification

**Dependencies**: Phase 2 complete

**Verification**:
- GET /health returns 200 OK
- JWT verification function works correctly
- Database tables created successfully

**Estimated Duration**: 1-1.5 hours

---

### Phase 4: Better Auth Configuration (Tasks Phase)

**Purpose**: Configure Better Auth with JWT plugin for frontend authentication.

**Tasks** (to be detailed in tasks.md):
- Create lib/auth.ts with Better Auth JWT plugin configuration
- Configure email/password provider
- Set session expiry (7 days for "Remember me", session-based otherwise)
- Create lib/api-client.ts with Axios instance and JWT interceptor
- Create components/auth/AuthContext.tsx for global auth state

**Dependencies**: Phase 2 complete

**Verification**:
- Better Auth configuration exports correctly
- Axios interceptor attaches JWT to requests
- 401 errors trigger redirect to sign-in

**Estimated Duration**: 45-60 minutes

---

### Phase 5: Landing Page (Tasks Phase)

**Purpose**: Create responsive landing page with hero, features, and CTA sections.

**Tasks** (to be detailed in tasks.md):
- Install shadcn/ui components (button, card)
- Create components/landing/Hero.tsx with gradient background
- Create components/landing/Features.tsx with 3 feature cards
- Create components/landing/CTA.tsx with sign-up call-to-action
- Create app/page.tsx assembling all landing components
- Add TailwindCSS gradient styles and scroll/hover animations

**Dependencies**: Phase 2 complete

**Verification**:
- Landing page loads in <2 seconds
- Responsive on mobile (375px), tablet (768px), desktop (1440px)
- All navigation links work correctly
- Animations smooth and performant

**Estimated Duration**: 1.5-2 hours

---

### Phase 6: Sign-Up Flow (Tasks Phase)

**Purpose**: Implement user registration with validation and JWT issuance.

**Tasks** (to be detailed in tasks.md):
- Install shadcn/ui form components (input, label, card)
- Create components/auth/SignUpForm.tsx with form fields
- Add client-side validation (email format, password strength, password match)
- Integrate Better Auth sign-up API
- Create app/signup/page.tsx
- Add error handling, loading states, and password visibility toggle
- Implement redirect to dashboard on success

**Dependencies**: Phase 4 complete

**Verification**:
- User can create account with valid data
- JWT token issued and stored
- Validation errors display inline
- Duplicate email rejected
- Redirect to dashboard works

**Estimated Duration**: 1.5-2 hours

---

### Phase 7: Sign-In Flow (Tasks Phase)

**Purpose**: Implement user authentication with credential verification.

**Tasks** (to be detailed in tasks.md):
- Create components/auth/SignInForm.tsx with email and password fields
- Add client-side validation
- Integrate Better Auth sign-in API
- Create app/signin/page.tsx
- Add "Remember me" checkbox functionality (7-day session)
- Add password visibility toggle
- Link between sign-up and sign-in pages
- Add "Forgot password?" link (non-functional placeholder)

**Dependencies**: Phase 4 and Phase 6 complete

**Verification**:
- User can sign in with valid credentials
- Invalid credentials show generic error
- JWT token issued and stored
- "Remember me" extends session to 7 days
- Redirect to dashboard works

**Estimated Duration**: 1-1.5 hours

---

### Phase 8: Protected Dashboard (Tasks Phase)

**Purpose**: Create protected dashboard with authentication verification.

**Tasks** (to be detailed in tasks.md):
- Create app/dashboard/page.tsx
- Add authentication check (redirect to sign-in if no token)
- Create sign-out functionality
- Add user profile menu with name display
- Add placeholder content for future task features
- Test redirect behavior for unauthenticated access

**Dependencies**: Phase 7 complete

**Verification**:
- Dashboard requires authentication
- Unauthenticated users redirected to sign-in
- Sign-out clears token and redirects
- User name displayed correctly

**Estimated Duration**: 45-60 minutes

---

### Phase 9: JWT Integration & Testing (Tasks Phase)

**Purpose**: Verify end-to-end JWT authentication flow.

**Tasks** (to be detailed in tasks.md):
- Verify Axios interceptor attaches JWT to all protected requests
- Test backend JWT verification on protected endpoints
- Test 401 error handling (automatic redirect to sign-in)
- Test token expiration behavior
- Test user_id matching in URLs (future task endpoints)
- Create two test users and verify data isolation

**Dependencies**: Phase 3, Phase 7, and Phase 8 complete

**Verification**:
- All API calls include JWT in Authorization header
- Backend verifies JWT correctly
- 401 errors trigger redirect
- Token expiration handled gracefully
- User data isolation enforced

**Estimated Duration**: 1-1.5 hours

---

## Total Implementation Estimate

**Total Phases**: 8 implementation phases (after Phase 0 research and Phase 1 design)
**Total Estimated Duration**: 8-11 hours of implementation work
**Critical Path**: Phase 2 → Phase 3 → Phase 4 → Phase 6 → Phase 7 → Phase 8 → Phase 9

**Parallel Opportunities**:
- Phase 5 (Landing Page) can be developed in parallel with Phase 3 (Backend Foundation)
- Phase 4 (Better Auth Config) can be developed in parallel with Phase 3 (Backend Foundation)

**MVP Milestone**: After Phase 5, Phase 6, and Phase 7, users can discover the app, sign up, and sign in (core authentication flow complete)

## Risk Assessment

**High Risk**:
- Better Auth JWT plugin configuration complexity (mitigation: thorough research in Phase 0)
- Neon PostgreSQL connection pooling issues (mitigation: use recommended asyncpg configuration)

**Medium Risk**:
- JWT token storage security (mitigation: research httpOnly cookies vs localStorage trade-offs)
- CORS configuration between frontend and backend (mitigation: explicit origin configuration)

**Low Risk**:
- shadcn/ui component customization (mitigation: well-documented library)
- TailwindCSS responsive design (mitigation: mobile-first approach)

## Next Steps

1. ✅ Complete Phase 0: Generate research.md
2. ✅ Complete Phase 1: Generate data-model.md, contracts/, quickstart.md
3. ⏭️ Run `/sp.tasks` to generate detailed task breakdown (tasks.md)
4. ⏭️ Execute tasks via Claude Code following constitution workflow
