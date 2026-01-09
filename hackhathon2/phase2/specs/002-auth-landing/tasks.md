---

description: "Task list for authentication and landing page implementation"
---

# Tasks: Authentication and Landing Page

**Input**: Design documents from `/specs/002-auth-landing/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - not included in this feature (no TDD requested in specification)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/app/`, `frontend/components/`
- Paths shown below follow web application structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency installation

- [ ] T001 Create backend directory structure (backend/src/, backend/tests/)
- [ ] T002 Create backend requirements.txt with FastAPI, SQLModel, PyJWT, Passlib, python-dotenv, asyncpg dependencies
- [ ] T003 Create backend Python virtual environment and install dependencies
- [ ] T004 Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, JWT_ALGORITHM, FRONTEND_URL placeholders
- [ ] T005 Create backend/.env with actual Neon PostgreSQL connection string and shared secret
- [ ] T006 [P] Install frontend dependencies: better-auth, axios, lucide-react
- [ ] T007 [P] Initialize shadcn/ui in frontend with default configuration
- [ ] T008 [P] Install shadcn/ui components: button, input, label, card
- [ ] T009 [P] Create frontend/.env.example with BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_API_URL placeholders
- [ ] T010 [P] Create frontend/.env.local with actual values matching backend secret
- [ ] T011 Update backend/.gitignore to exclude .env, venv/, __pycache__/
- [ ] T012 Update frontend/.gitignore to exclude .env.local, .env*.local

**Checkpoint**: Dependencies installed, environment variables configured, secrets match between frontend and backend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T013 Create backend/src/__init__.py (empty file for Python package)
- [ ] T014 Create backend/src/database.py with async SQLModel engine and Neon PostgreSQL connection
- [ ] T015 Create backend/src/models.py with User SQLModel class (id, email, password_hash, name, created_at)
- [ ] T016 [P] Add Task SQLModel class to backend/src/models.py (id, user_id, title, description, completed, created_at)
- [ ] T017 Create database tables by running SQLModel metadata.create_all() in backend/src/database.py
- [ ] T018 Create backend/src/auth.py with verify_jwt_token() function using PyJWT
- [ ] T019 Add get_current_user() dependency function to backend/src/auth.py for FastAPI route protection
- [ ] T020 Create backend/src/main.py with FastAPI app initialization
- [ ] T021 Add CORS middleware to backend/src/main.py allowing frontend origin with credentials
- [ ] T022 Add GET /health endpoint to backend/src/main.py returning status, timestamp, version, database connection
- [ ] T023 Add POST /auth/signup endpoint to backend/src/main.py with email/password validation and bcrypt hashing
- [ ] T024 Add POST /auth/signin endpoint to backend/src/main.py with credential verification and JWT issuance
- [ ] T025 Add GET /auth/verify endpoint to backend/src/main.py with JWT validation
- [ ] T026 Test backend server starts successfully with uvicorn and /health returns 200
- [ ] T027 Create frontend/lib/auth.ts with Better Auth configuration and JWT plugin
- [ ] T028 Configure email/password provider in frontend/lib/auth.ts with 7-day session expiry
- [ ] T029 Create frontend/lib/api-client.ts with Axios instance using NEXT_PUBLIC_API_URL
- [ ] T030 Add JWT interceptor to frontend/lib/api-client.ts to attach token to all requests
- [ ] T031 Add 401 error interceptor to frontend/lib/api-client.ts to redirect to /signin
- [ ] T032 Create frontend/components/auth/AuthContext.tsx with React Context for global auth state
- [ ] T033 Add AuthProvider to frontend/app/layout.tsx wrapping children

**Checkpoint**: Foundation ready - backend API running, database connected, Better Auth configured, user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - First-Time Visitor Discovery (Priority: P1) 🎯 MVP

**Goal**: Create responsive landing page with hero, features, and CTA sections that loads in <2 seconds

**Independent Test**: Visit http://localhost:3000 and verify landing page displays with all sections, responsive on mobile/tablet/desktop, navigation links work

- [ ] T034 [P] [US1] Create frontend/components/landing/Hero.tsx with gradient background, app name, tagline, "Get Started" and "Sign In" buttons
- [ ] T035 [P] [US1] Create frontend/components/landing/Features.tsx with 3 feature cards (Quick Creation, Stay Organized, Sync Everywhere) using Lucide icons
- [ ] T036 [P] [US1] Create frontend/components/landing/CTA.tsx with "Ready to Get Started?" heading and sign-up button
- [ ] T037 [US1] Create frontend/app/page.tsx assembling Hero, Features, and CTA components
- [ ] T038 [US1] Add TailwindCSS blue-purple gradient styles to frontend/app/page.tsx and landing components
- [ ] T039 [US1] Add responsive grid layout to Features component (3 columns desktop, 2 tablet, 1 mobile)
- [ ] T040 [US1] Add smooth scroll and hover animations to landing page components
- [ ] T041 [US1] Add navigation links from Hero buttons to /signup and /signin routes
- [ ] T042 [US1] Test landing page loads in <2 seconds and is responsive on 375px, 768px, 1440px viewports

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - landing page is live and navigable

---

## Phase 4: User Story 2 - New User Account Creation (Priority: P2)

**Goal**: Implement sign-up flow with validation, JWT issuance, and dashboard redirect

**Independent Test**: Navigate to /signup, create account with valid data, verify JWT stored and redirected to /dashboard

- [ ] T043 [P] [US2] Create frontend/components/auth/SignUpForm.tsx with email, password, confirmPassword, name fields
- [ ] T044 [US2] Add client-side email format validation to SignUpForm using regex
- [ ] T045 [US2] Add client-side password validation to SignUpForm (minimum 8 characters)
- [ ] T046 [US2] Add password strength indicator to SignUpForm showing weak/medium/strong
- [ ] T047 [US2] Add confirmPassword matching validation to SignUpForm
- [ ] T048 [US2] Add password visibility toggle icon button to SignUpForm password fields
- [ ] T049 [US2] Add inline error messages below each field in SignUpForm
- [ ] T050 [US2] Add loading state to SignUpForm submit button (disabled with spinner)
- [ ] T051 [US2] Integrate Better Auth signup API call in SignUpForm onSubmit handler
- [ ] T052 [US2] Add error handling in SignUpForm for duplicate email (409) and validation errors (400)
- [ ] T053 [US2] Add success handler in SignUpForm to store JWT and redirect to /dashboard
- [ ] T054 [US2] Create frontend/app/signup/page.tsx with centered card layout containing SignUpForm
- [ ] T055 [US2] Add "Already have an account? Sign in" link to signup page
- [ ] T056 [US2] Test sign-up flow: create user, verify JWT stored, verify redirect to dashboard

**Checkpoint**: At this point, User Story 2 should be fully functional and testable independently - users can create accounts and get authenticated

---

## Phase 5: User Story 3 - Returning User Authentication (Priority: P3)

**Goal**: Implement sign-in flow with credential verification, "Remember me", and dashboard redirect

**Independent Test**: Navigate to /signin, authenticate with valid credentials, verify JWT stored and redirected to /dashboard

- [ ] T057 [P] [US3] Create frontend/components/auth/SignInForm.tsx with email, password, rememberMe fields
- [ ] T058 [US3] Add client-side email format validation to SignInForm
- [ ] T059 [US3] Add password visibility toggle icon button to SignInForm
- [ ] T060 [US3] Add "Remember me" checkbox to SignInForm (extends session to 7 days)
- [ ] T061 [US3] Add inline error messages to SignInForm
- [ ] T062 [US3] Add loading state to SignInForm submit button (disabled with spinner)
- [ ] T063 [US3] Integrate Better Auth signin API call in SignInForm onSubmit handler
- [ ] T064 [US3] Add error handling in SignInForm for invalid credentials (401) showing generic error
- [ ] T065 [US3] Add success handler in SignInForm to store JWT and redirect to /dashboard
- [ ] T066 [US3] Create frontend/app/signin/page.tsx with centered card layout containing SignInForm
- [ ] T067 [US3] Add "Don't have an account? Sign up" link to signin page
- [ ] T068 [US3] Add "Forgot password?" link to signin page (non-functional placeholder)
- [ ] T069 [US3] Test sign-in flow: authenticate user, verify JWT stored, verify redirect to dashboard
- [ ] T070 [US3] Test "Remember me" functionality extends session to 7 days

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently - complete authentication flow functional

---

## Phase 6: User Story 4 - Protected Content Access (Priority: P4)

**Goal**: Create protected dashboard with authentication verification and sign-out functionality

**Independent Test**: Access /dashboard without auth (redirected to /signin), access with auth (dashboard loads), sign out (redirected to landing page)

- [ ] T071 [US4] Create frontend/app/dashboard/page.tsx with authentication check using AuthContext
- [ ] T072 [US4] Add redirect logic to dashboard page: if no JWT, redirect to /signin
- [ ] T073 [US4] Add dashboard header with user name display from JWT claims
- [ ] T074 [US4] Add sign-out button to dashboard header
- [ ] T075 [US4] Implement sign-out handler: clear JWT, clear AuthContext, redirect to landing page
- [ ] T076 [US4] Add user profile menu to dashboard with name and email display
- [ ] T077 [US4] Add placeholder content to dashboard for future task features
- [ ] T078 [US4] Test unauthenticated access to /dashboard redirects to /signin
- [ ] T079 [US4] Test authenticated access to /dashboard loads successfully
- [ ] T080 [US4] Test sign-out clears token and redirects to landing page
- [ ] T081 [US4] Test expired token triggers redirect to /signin when accessing dashboard

**Checkpoint**: All user stories should now be independently functional - complete authentication system with protected content

---

## Phase 7: Integration & End-to-End Validation

**Purpose**: Verify complete authentication flow and cross-story integration

- [ ] T082 Verify Axios interceptor attaches JWT to all API requests in browser DevTools Network tab
- [ ] T083 Test backend JWT verification on /auth/verify endpoint with valid and invalid tokens
- [ ] T084 Test 401 error handling: make request with expired token, verify auto-redirect to /signin
- [ ] T085 Test token expiration: wait for token to expire, verify redirect on next protected request
- [ ] T086 Create two test users (User A and User B) via sign-up flow
- [ ] T087 Verify User A can sign in and access dashboard with their credentials
- [ ] T088 Verify User B can sign in and access dashboard with their credentials
- [ ] T089 Test authenticated user cannot access /signup or /signin (should redirect to /dashboard)
- [ ] T090 Test landing page navigation: click "Get Started" → /signup, click "Sign In" → /signin
- [ ] T091 Test sign-up to sign-in flow: create account, sign out, sign in with same credentials
- [ ] T092 Test responsive design: verify all pages work on mobile (375px), tablet (768px), desktop (1440px)
- [ ] T093 Test form validation: submit empty forms, invalid emails, short passwords, mismatched passwords
- [ ] T094 Test error handling: disconnect backend, verify frontend shows appropriate errors
- [ ] T095 Test landing page load time: verify <2 seconds with browser Performance tab

**Checkpoint**: Complete authentication system validated end-to-end with all user stories working together

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T096 [P] Create backend/README.md with setup instructions, API endpoints, environment variables
- [ ] T097 [P] Create frontend/README.md with setup instructions, available routes, environment variables
- [ ] T098 [P] Verify all .env files are in .gitignore and not committed
- [ ] T099 [P] Verify .env.example files have all required variables with placeholder values
- [ ] T100 [P] Add TypeScript types for User and AuthResponse in frontend/lib/types.ts
- [ ] T101 [P] Add Python type hints to all functions in backend/src/ files
- [ ] T102 Run frontend TypeScript compiler (tsc --noEmit) and fix any type errors
- [ ] T103 Run backend type checker (mypy) and fix any type errors
- [ ] T104 Test all constitution quality gates from specs/002-auth-landing/checklists/requirements.md
- [ ] T105 Run quickstart.md validation: follow setup guide from scratch, verify all steps work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational - No dependencies on other stories
  - User Story 3 (P3): Can start after Foundational - No dependencies on other stories
  - User Story 4 (P4): Depends on Foundational - Should be after US2 and US3 for testing
- **Integration (Phase 7)**: Depends on all user stories being complete
- **Polish (Phase 8)**: Depends on Integration completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - Independently testable
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Integrates with US2 and US3 but independently testable

### Within Each User Story

- Tasks within a story marked [P] can run in parallel
- Tasks without [P] should run sequentially in order
- Complete all tasks in a story before moving to next priority

### Parallel Opportunities

- **Setup Phase**: T006-T010 can run in parallel (frontend tasks), T011-T012 can run in parallel
- **Foundational Phase**: T015-T016 can run in parallel (models), T027-T033 can run in parallel (frontend auth config)
- **User Story 1**: T034-T036 can run in parallel (landing components)
- **User Story 2**: T043 can start immediately, other tasks sequential
- **User Story 3**: T057 can start immediately, other tasks sequential
- **User Story 4**: All tasks sequential (depend on auth state)
- **Polish Phase**: T096-T101 can run in parallel (documentation and types)

---

## Parallel Example: User Story 1 (Landing Page)

```bash
# Launch all landing page components together:
Task T034: "Create Hero.tsx with gradient background and CTA buttons"
Task T035: "Create Features.tsx with 3 feature cards and icons"
Task T036: "Create CTA.tsx with sign-up call-to-action"

# Then assemble sequentially:
Task T037: "Create page.tsx assembling all components"
Task T038: "Add TailwindCSS gradient styles"
Task T039: "Add responsive grid layout"
Task T040: "Add animations"
Task T041: "Add navigation links"
Task T042: "Test responsiveness and load time"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Landing Page)
4. **STOP and VALIDATE**: Test landing page independently
5. Deploy/demo if ready

**MVP Deliverable**: Responsive landing page with navigation to auth pages (even if auth pages don't exist yet)

### Incremental Delivery (Recommended)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Landing page live!)
3. Add User Story 2 → Test independently → Deploy/Demo (Sign-up working!)
4. Add User Story 3 → Test independently → Deploy/Demo (Sign-in working!)
5. Add User Story 4 → Test independently → Deploy/Demo (Protected dashboard working!)
6. Complete Integration → Test end-to-end → Deploy/Demo (Full auth system!)
7. Complete Polish → Final validation → Production ready

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Landing Page)
   - Developer B: User Story 2 (Sign-Up)
   - Developer C: User Story 3 (Sign-In)
3. Developer D: User Story 4 after US2 and US3 complete
4. Team: Integration and Polish together

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 105 tasks
**Setup Phase**: 12 tasks
**Foundational Phase**: 21 tasks (BLOCKING)
**User Story 1 (P1)**: 9 tasks
**User Story 2 (P2)**: 14 tasks
**User Story 3 (P3)**: 14 tasks
**User Story 4 (P4)**: 11 tasks
**Integration Phase**: 14 tasks
**Polish Phase**: 10 tasks

**Parallel Opportunities**: 25+ tasks can run in parallel across phases
**Critical Path**: Setup → Foundational → US2 → US3 → US4 → Integration → Polish
**MVP Path**: Setup → Foundational → US1 (Landing Page only)
