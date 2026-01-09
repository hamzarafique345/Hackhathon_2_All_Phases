# Research: Authentication and Landing Page

**Feature**: 002-auth-landing
**Date**: 2026-01-08
**Purpose**: Validate technology choices and document best practices for implementation

## Research Topics

### 1. Better Auth JWT Plugin Configuration for Next.js 16 App Router

**Decision**: Use Better Auth v1.x with JWT plugin for authentication

**Research Findings**:
- Better Auth supports Next.js 13+ App Router with server actions and API routes
- JWT plugin enables stateless authentication suitable for API-based architecture
- Configuration requires `auth.ts` in `/lib` directory with plugin exports
- Supports email/password provider out of the box
- Session management configurable (session-based or persistent with expiry)

**Configuration Approach**:
```typescript
// lib/auth.ts structure
import { betterAuth } from "better-auth"
import { jwt } from "better-auth/plugins"

export const auth = betterAuth({
  database: { ... },
  emailAndPassword: { enabled: true },
  plugins: [jwt({ expiresIn: "7d" })],
  secret: process.env.BETTER_AUTH_SECRET
})
```

**Rationale**: Better Auth provides type-safe authentication with minimal boilerplate, integrates seamlessly with Next.js App Router, and supports JWT tokens required by the constitution.

**Alternatives Considered**:
- NextAuth.js: More mature but heavier, less type-safe
- Clerk: Third-party service, adds external dependency and cost
- Custom JWT implementation: More control but higher maintenance burden

**References**:
- Better Auth documentation: https://better-auth.com
- JWT plugin docs: https://better-auth.com/docs/plugins/jwt

---

### 2. FastAPI + SQLModel Best Practices for Async PostgreSQL

**Decision**: Use FastAPI with SQLModel and asyncpg for async database operations

**Research Findings**:
- SQLModel combines SQLAlchemy ORM with Pydantic validation
- asyncpg is the fastest PostgreSQL driver for Python
- FastAPI supports async/await natively for non-blocking I/O
- SQLModel provides type hints that work with FastAPI automatic validation
- Connection pooling handled by SQLAlchemy async engine

**Implementation Approach**:
```python
# database.py structure
from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

DATABASE_URL = os.getenv("DATABASE_URL")
# Convert postgres:// to postgresql+asyncpg://
async_url = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")

engine = create_async_engine(async_url, echo=True, pool_size=5)
```

**Best Practices**:
- Use async session management with context managers
- Define models with SQLModel (inherits from SQLAlchemy Base + Pydantic BaseModel)
- Use dependency injection for database sessions
- Enable connection pooling (default pool_size=5 for Neon)
- Use Alembic for migrations (future phase)

**Rationale**: SQLModel provides type safety across database and API layers, asyncpg offers best performance, and FastAPI's async support enables high concurrency.

**Alternatives Considered**:
- Tortoise ORM: Less mature, smaller ecosystem
- Raw asyncpg: More control but loses ORM benefits and type safety
- Sync SQLAlchemy: Simpler but blocks on I/O, lower throughput

**References**:
- SQLModel documentation: https://sqlmodel.tiangolo.com
- FastAPI async SQL: https://fastapi.tiangolo.com/advanced/async-sql-databases/

---

### 3. Neon PostgreSQL Connection Pooling and Configuration

**Decision**: Use Neon's connection pooling with asyncpg driver

**Research Findings**:
- Neon provides serverless PostgreSQL with automatic connection pooling
- Connection string format: `postgresql://user:pass@host/db?sslmode=require`
- Neon supports both pooled and direct connections
- Pooled connection recommended for serverless/edge deployments
- SSL required for all connections (sslmode=require)

**Configuration Approach**:
```python
# Use Neon's pooled connection endpoint
DATABASE_URL = "postgresql+asyncpg://user:pass@ep-xxx.neon.tech/dbname?sslmode=require"

# SQLAlchemy engine configuration
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries in development
    pool_size=5,  # Connection pool size
    max_overflow=10,  # Additional connections when pool exhausted
    pool_pre_ping=True,  # Verify connections before use
)
```

**Best Practices**:
- Use pooled connection endpoint (not direct)
- Enable SSL (required by Neon)
- Set reasonable pool_size (5-10 for typical apps)
- Enable pool_pre_ping to handle stale connections
- Use connection timeouts to prevent hanging

**Rationale**: Neon's serverless architecture requires connection pooling for efficiency. Pooled connections reduce latency and handle connection limits automatically.

**Alternatives Considered**:
- Direct connections: Higher latency, connection limit issues
- External pooler (PgBouncer): Adds complexity, unnecessary with Neon's built-in pooling
- Supabase: Similar offering but Neon chosen per constitution

**References**:
- Neon documentation: https://neon.tech/docs
- Connection pooling guide: https://neon.tech/docs/connect/connection-pooling

---

### 4. shadcn/ui Component Installation and Customization

**Decision**: Use shadcn/ui for UI components with TailwindCSS

**Research Findings**:
- shadcn/ui is not a component library but a collection of reusable components
- Components copied into project (not npm package), full ownership
- Built on Radix UI primitives for accessibility
- Fully customizable with TailwindCSS
- TypeScript-first with excellent type safety

**Installation Approach**:
```bash
# Initialize shadcn/ui
npx shadcn-ui@latest init

# Install specific components as needed
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add label
npx shadcn-ui@latest add card
```

**Component Structure**:
- Components installed to `components/ui/`
- Each component is a single file (e.g., `button.tsx`)
- Customization via TailwindCSS classes
- Variants defined using `class-variance-authority`

**Customization for Blue-Purple Gradient**:
```typescript
// tailwind.config.ts
theme: {
  extend: {
    colors: {
      primary: {
        DEFAULT: '#3B82F6', // Blue
        gradient: 'linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%)'
      }
    }
  }
}
```

**Rationale**: shadcn/ui provides high-quality, accessible components with full customization. Copy-paste approach avoids dependency bloat and version conflicts.

**Alternatives Considered**:
- Material-UI: Heavier, opinionated design system
- Chakra UI: Good but less customizable
- Headless UI: Lower-level, more work to style
- Custom components: More work, reinventing the wheel

**References**:
- shadcn/ui documentation: https://ui.shadcn.com
- Installation guide: https://ui.shadcn.com/docs/installation/next

---

### 5. JWT Token Storage Strategies (httpOnly Cookies vs localStorage)

**Decision**: Use httpOnly cookies for JWT storage (primary), with localStorage as fallback for development

**Research Findings**:
- **httpOnly cookies**: Immune to XSS attacks, automatically sent with requests, requires CORS configuration
- **localStorage**: Vulnerable to XSS, requires manual attachment to requests, simpler CORS
- **sessionStorage**: Same as localStorage but cleared on tab close
- Better Auth supports both strategies via configuration

**Security Comparison**:

| Strategy | XSS Protection | CSRF Protection | Ease of Use | Mobile Support |
|----------|----------------|-----------------|-------------|----------------|
| httpOnly cookies | ✅ Excellent | ⚠️ Needs CSRF token | Medium | ✅ Good |
| localStorage | ❌ Vulnerable | ✅ Not applicable | Easy | ✅ Good |
| sessionStorage | ❌ Vulnerable | ✅ Not applicable | Easy | ✅ Good |

**Implementation Approach**:
```typescript
// lib/auth.ts
export const auth = betterAuth({
  // ... other config
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 60 * 60 * 24 * 7 // 7 days
    }
  },
  advanced: {
    useSecureCookies: process.env.NODE_ENV === "production",
    cookieOptions: {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax"
    }
  }
})
```

**CORS Configuration Required**:
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,  # Required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Rationale**: httpOnly cookies provide superior XSS protection, which is critical for authentication tokens. The CORS complexity is manageable and worth the security benefit.

**Alternatives Considered**:
- localStorage only: Simpler but vulnerable to XSS attacks
- sessionStorage: Loses session on tab close, poor UX
- Encrypted localStorage: Still vulnerable to XSS, adds complexity

**Trade-offs**:
- httpOnly cookies require CORS configuration with credentials
- Cannot access token from JavaScript (by design, for security)
- Requires backend to set cookies (Better Auth handles this)

**References**:
- OWASP JWT storage: https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html
- Better Auth session docs: https://better-auth.com/docs/concepts/session

---

## Summary of Decisions

| Topic | Decision | Primary Rationale |
|-------|----------|-------------------|
| Authentication | Better Auth with JWT plugin | Type-safe, Next.js 16 compatible, minimal boilerplate |
| Backend Framework | FastAPI + SQLModel + asyncpg | Type safety, async performance, Pydantic integration |
| Database | Neon PostgreSQL with pooling | Serverless, automatic pooling, SSL by default |
| UI Components | shadcn/ui with TailwindCSS | Full customization, accessibility, no dependency bloat |
| Token Storage | httpOnly cookies (primary) | XSS protection, automatic request inclusion |

## Implementation Risks & Mitigations

**Risk 1: Better Auth JWT plugin complexity**
- Mitigation: Follow official documentation closely, test authentication flow early
- Fallback: Use Better Auth's default session strategy if JWT proves problematic

**Risk 2: Neon connection pooling issues**
- Mitigation: Use recommended asyncpg configuration, enable pool_pre_ping
- Fallback: Increase pool_size if connection exhaustion occurs

**Risk 3: CORS configuration for httpOnly cookies**
- Mitigation: Set allow_credentials=True, specify exact origin (not wildcard)
- Fallback: Use localStorage for development if CORS issues persist

**Risk 4: JWT token expiration handling**
- Mitigation: Implement automatic redirect on 401, clear expired tokens
- Fallback: Prompt user to re-authenticate with clear messaging

## Technology Versions

**Frontend**:
- Next.js: 16.x (latest stable)
- Better Auth: 1.x (latest)
- TypeScript: 5.x
- TailwindCSS: 3.x
- shadcn/ui: Latest (no version, copy-paste)

**Backend**:
- Python: 3.11+
- FastAPI: 0.110+
- SQLModel: 0.0.14+
- PyJWT: 2.8+
- Passlib: 1.7+
- asyncpg: 0.29+

**Database**:
- PostgreSQL: 15+ (Neon managed)

## Next Steps

1. ✅ Research complete - all technology choices validated
2. ⏭️ Proceed to Phase 1: Create data-model.md, contracts/, quickstart.md
3. ⏭️ After Phase 1: Run `/sp.tasks` to generate task breakdown
