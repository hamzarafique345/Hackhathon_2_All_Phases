# Data Model: Authentication and Landing Page

**Feature**: 002-auth-landing
**Date**: 2026-01-08
**Purpose**: Define entities, relationships, and validation rules for authentication system

## Entity Definitions

### User Entity

**Purpose**: Represents a registered user account in the system.

**Attributes**:

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT gen_random_uuid() | Unique identifier for the user |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address (used for authentication) |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hash of user's password (never store plain text) |
| name | VARCHAR(255) | NULLABLE | User's display name (optional) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

**Validation Rules**:
- **email**: Must be valid email format (RFC 5322), case-insensitive uniqueness
- **password_hash**: Must be bcrypt hash with minimum 12 rounds (enforced at application level)
- **name**: If provided, must be 1-255 characters, trimmed of whitespace
- **created_at**: Automatically set on creation, immutable

**Indexes**:
- PRIMARY KEY on `id` (automatic)
- UNIQUE INDEX on `email` (for fast lookup and duplicate prevention)

**Business Rules**:
- Email addresses are case-insensitive (normalize to lowercase before storage)
- Password must be minimum 8 characters before hashing (enforced at application level)
- Users cannot change their email after registration (future enhancement)
- Soft delete not implemented (hard delete only)

**Security Considerations**:
- Password never stored in plain text
- Bcrypt hash includes salt automatically
- Email used as username (no separate username field)
- No password history tracking (future enhancement)

---

### Task Entity

**Purpose**: Represents a todo item belonging to a specific user.

**Attributes**:

| Attribute | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL, DEFAULT gen_random_uuid() | Unique identifier for the task |
| user_id | UUID | FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE, NOT NULL | Owner of the task |
| title | VARCHAR(255) | NOT NULL | Task title/summary |
| description | TEXT | NULLABLE | Detailed task description (optional) |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Task creation timestamp |

**Validation Rules**:
- **user_id**: Must reference existing user, cannot be null
- **title**: Must be 1-255 characters, cannot be empty or whitespace-only
- **description**: If provided, maximum 10,000 characters
- **completed**: Boolean only (true/false), defaults to false
- **created_at**: Automatically set on creation, immutable

**Indexes**:
- PRIMARY KEY on `id` (automatic)
- INDEX on `user_id` (for fast user task lookups)
- INDEX on `created_at` (for chronological sorting)
- COMPOSITE INDEX on `(user_id, created_at)` (optimized for user's task list queries)

**Business Rules**:
- Tasks always belong to exactly one user
- Deleting a user cascades to delete all their tasks
- Tasks cannot be transferred between users
- No task sharing or collaboration (future enhancement)
- Completed tasks remain in the system (no auto-archival)

**Security Considerations**:
- All task queries MUST filter by user_id to enforce data isolation
- API endpoints MUST verify JWT user_id matches task owner
- No public or shared tasks (all private to owner)

---

## Entity Relationships

```
User (1) ──────< (N) Task
  │                   │
  │                   │
  └─ One user can have many tasks
                      │
                      └─ Each task belongs to exactly one user
```

**Relationship Type**: One-to-Many (User → Task)

**Cardinality**:
- One User can have zero or many Tasks
- One Task belongs to exactly one User

**Referential Integrity**:
- Foreign key constraint enforces user_id references valid user
- ON DELETE CASCADE ensures orphaned tasks are deleted when user is deleted
- No ON UPDATE CASCADE (user IDs are immutable)

**Query Patterns**:
- Get all tasks for a user: `SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC`
- Get user with task count: `SELECT u.*, COUNT(t.id) FROM users u LEFT JOIN tasks t ON u.id = t.user_id GROUP BY u.id`
- Get incomplete tasks: `SELECT * FROM tasks WHERE user_id = ? AND completed = false`

---

## State Transitions

### User Entity States

```
[Non-existent]
    │
    │ Sign-up (create account)
    ↓
[Active]
    │
    │ Delete account (future)
    ↓
[Deleted]
```

**State Rules**:
- Users are created in Active state
- No inactive or suspended states in this phase
- Deletion is permanent (no soft delete)

---

### Task Entity States

```
[Non-existent]
    │
    │ Create task
    ↓
[Incomplete] (completed = false)
    │
    │ Toggle completion
    ↓
[Complete] (completed = true)
    │
    │ Toggle completion
    ↓
[Incomplete]
    │
    │ Delete task
    ↓
[Deleted]
```

**State Rules**:
- Tasks created with completed = false
- Completion status can be toggled unlimited times
- No "archived" or "deleted" status (hard delete only)
- No task history tracking (future enhancement)

---

## Validation Summary

### User Validation (Application Level)

**Sign-Up Validation**:
```typescript
// Frontend validation
- email: required, valid format, max 255 chars
- password: required, min 8 chars, max 128 chars
- confirmPassword: required, must match password
- name: optional, max 255 chars

// Backend validation (duplicate checks)
- email: unique (case-insensitive)
- password: hashed with bcrypt (12 rounds minimum)
```

**Sign-In Validation**:
```typescript
// Frontend validation
- email: required, valid format
- password: required

// Backend validation
- email: exists in database
- password: matches stored hash
```

---

### Task Validation (Application Level)

**Create Task Validation**:
```typescript
// Frontend validation
- title: required, min 1 char, max 255 chars
- description: optional, max 10,000 chars

// Backend validation
- user_id: matches JWT claim
- title: not empty after trim
```

**Update Task Validation**:
```typescript
// Frontend validation
- title: required, min 1 char, max 255 chars
- description: optional, max 10,000 chars
- completed: boolean

// Backend validation
- user_id: matches JWT claim (authorization)
- task exists and belongs to user
```

---

## Database Schema (SQL)

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index for email lookups (case-insensitive)
CREATE UNIQUE INDEX idx_users_email_lower ON users (LOWER(email));

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for task queries
CREATE INDEX idx_tasks_user_id ON tasks (user_id);
CREATE INDEX idx_tasks_created_at ON tasks (created_at);
CREATE INDEX idx_tasks_user_created ON tasks (user_id, created_at);
```

---

## SQLModel Definitions (Python)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## TypeScript Types (Frontend)

```typescript
// User type (never includes password_hash)
export interface User {
  id: string;
  email: string;
  name: string | null;
  created_at: string; // ISO 8601 format
}

// Task type
export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string; // ISO 8601 format
}

// Sign-up request
export interface SignUpRequest {
  email: string;
  password: string;
  name?: string;
}

// Sign-in request
export interface SignInRequest {
  email: string;
  password: string;
  rememberMe?: boolean;
}

// Auth response
export interface AuthResponse {
  user: User;
  token: string;
  expiresAt: string;
}
```

---

## Data Migration Strategy

**Phase 1: Initial Schema**
- Create users table with all columns
- Create tasks table with all columns
- Create indexes for performance

**Future Phases** (not in this feature):
- Add email verification (verified_at column)
- Add password reset tokens (separate table)
- Add user preferences (separate table or JSONB column)
- Add task tags/categories (many-to-many relationship)
- Add task due dates (due_at column)

**Migration Tool**: Alembic (to be configured in future phase)

---

## Performance Considerations

**Expected Query Patterns**:
1. Get user by email (sign-in): O(1) with unique index
2. Get all tasks for user: O(n) where n = user's task count, optimized with composite index
3. Create task: O(1) insert
4. Update task: O(1) with primary key lookup
5. Delete task: O(1) with primary key lookup

**Optimization Strategies**:
- Composite index on (user_id, created_at) for sorted task lists
- Email stored in lowercase for case-insensitive lookups
- UUID primary keys for distributed systems and security
- Connection pooling for concurrent requests

**Scalability**:
- Current design supports 100,000+ users
- Task queries scoped to single user (no cross-user queries)
- Indexes ensure sub-100ms query times for typical workloads

---

## Security & Privacy

**Data Protection**:
- Passwords never stored in plain text (bcrypt hash only)
- User data isolated by user_id (enforced at application level)
- No personally identifiable information beyond email
- Email addresses not exposed in public APIs

**Compliance Considerations**:
- GDPR: Users can delete their account (cascade deletes all tasks)
- Data retention: No automatic deletion (user-initiated only)
- Data export: Not implemented in this phase (future enhancement)

**Audit Trail**:
- created_at timestamp for all entities
- No update timestamps in this phase (future enhancement)
- No audit log table (future enhancement)
