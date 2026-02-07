# Data Model: AI-Powered Todo Chatbot

**Feature**: 003-ai-chatbot
**Date**: 2026-01-24
**Status**: Complete

## Overview

This document defines the database schema and entity models for Phase 3 AI chatbot functionality. All new tables extend the existing Phase 2 schema without modifying Phase 2 tables (users, tasks).

---

## Database Schema

### Phase 2 Tables (Existing - Unchanged)

#### users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### tasks
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
```

---

### Phase 3 Tables (New)

#### conversations

Stores chat conversations between users and the AI assistant.

```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at);
```

**Fields**:
- `id`: Unique identifier for the conversation
- `user_id`: Foreign key to users table (owner of conversation)
- `title`: Optional conversation title (can be auto-generated from first message or user-provided)
- `created_at`: Timestamp when conversation was created
- `updated_at`: Timestamp of last message in conversation (updated on each new message)

**Constraints**:
- `user_id` MUST reference valid user (foreign key)
- Deleting user MUST cascade delete all their conversations
- `title` is optional (NULL allowed)

**Indexes**:
- `idx_conversations_user_id`: Fast lookup of user's conversations
- `idx_conversations_updated_at`: Sort conversations by recent activity

**Validation Rules**:
- `user_id`: Required, must exist in users table
- `title`: Optional, max 255 characters if provided
- `created_at`: Auto-generated, immutable
- `updated_at`: Auto-updated on message creation

---

#### messages

Stores individual messages within conversations (both user and AI messages).

```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_conversation_created ON messages(conversation_id, created_at);
```

**Fields**:
- `id`: Unique identifier for the message
- `conversation_id`: Foreign key to conversations table
- `role`: Message sender ('user' or 'assistant')
- `content`: Message text content
- `created_at`: Timestamp when message was created

**Constraints**:
- `conversation_id` MUST reference valid conversation (foreign key)
- `role` MUST be either 'user' or 'assistant' (CHECK constraint)
- `content` MUST NOT be empty (NOT NULL)
- Deleting conversation MUST cascade delete all messages

**Indexes**:
- `idx_messages_conversation_id`: Fast lookup of conversation messages
- `idx_messages_created_at`: Sort messages chronologically
- `idx_messages_conversation_created`: Composite index for efficient conversation message retrieval with ordering

**Validation Rules**:
- `conversation_id`: Required, must exist in conversations table
- `role`: Required, must be 'user' or 'assistant'
- `content`: Required, non-empty text
- `created_at`: Auto-generated, immutable

---

## Entity Relationships

```
users (Phase 2)
  ├── 1:N → tasks (Phase 2)
  └── 1:N → conversations (Phase 3)
                └── 1:N → messages (Phase 3)
```

**Relationship Details**:
- One user has many conversations
- One conversation has many messages
- One user has many tasks (Phase 2, unchanged)
- Conversations and tasks are independent (no direct relationship)

**Cascade Behavior**:
- Delete user → cascade delete conversations → cascade delete messages
- Delete user → cascade delete tasks (Phase 2, unchanged)
- Delete conversation → cascade delete messages

---

## SQLModel Definitions (Python)

### Conversation Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    title: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

### Message Model

```python
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(
        foreign_key="conversations.id",
        nullable=False,
        index=True
    )
    role: MessageRole = Field(nullable=False)
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

### Extended User Model (Phase 2 + Phase 3)

```python
# Extend existing Phase 2 User model with Phase 3 relationship
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    password_hash: str = Field(nullable=False, max_length=255)
    name: str = Field(nullable=False, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Phase 2 relationships (existing)
    tasks: List["Task"] = Relationship(back_populates="user")

    # Phase 3 relationships (new)
    conversations: List[Conversation] = Relationship(back_populates="user")
```

---

## API Request/Response Models (Pydantic)

### Conversation DTOs

```python
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional, List

class ConversationCreate(BaseModel):
    """Request body for creating a conversation"""
    title: Optional[str] = None

class ConversationResponse(BaseModel):
    """Response for conversation data"""
    id: UUID
    user_id: UUID
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    message_count: Optional[int] = None  # Optional: include message count

class ConversationListResponse(BaseModel):
    """Response for listing conversations"""
    conversations: List[ConversationResponse]
    total: int
```

### Message DTOs

```python
class MessageCreate(BaseModel):
    """Request body for creating a message"""
    role: MessageRole
    content: str

class MessageResponse(BaseModel):
    """Response for message data"""
    id: UUID
    conversation_id: UUID
    role: MessageRole
    content: str
    created_at: datetime

class MessageListResponse(BaseModel):
    """Response for listing messages"""
    messages: List[MessageResponse]
    total: int
    conversation_id: UUID
```

---

## Data Validation Rules

### Conversation Validation

- **user_id**: Must exist in users table
- **title**: Optional, max 255 characters, trimmed
- **created_at**: Auto-generated, cannot be modified
- **updated_at**: Auto-updated on message creation

### Message Validation

- **conversation_id**: Must exist in conversations table
- **role**: Must be 'user' or 'assistant'
- **content**: Required, non-empty, max 10,000 characters (prevent abuse)
- **created_at**: Auto-generated, cannot be modified

### Business Rules

1. **User Isolation**: Users can only access their own conversations
2. **Message Ordering**: Messages ordered by created_at within conversation
3. **Conversation Updates**: updated_at timestamp updated when new message added
4. **Cascade Deletion**: Deleting conversation deletes all messages
5. **Empty Conversations**: Conversations can exist without messages (created but not yet used)

---

## Migration Strategy

### Alembic Migration

```python
"""Add conversations and messages tables for Phase 3 AI chatbot

Revision ID: 003_ai_chatbot
Revises: 002_phase2_complete
Create Date: 2026-01-24
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', UUID(), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_updated_at', 'conversations', ['updated_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', UUID(), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('conversation_id', UUID(), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='check_message_role'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])
    op.create_index('idx_messages_conversation_created', 'messages', ['conversation_id', 'created_at'])

def downgrade():
    op.drop_index('idx_messages_conversation_created', 'messages')
    op.drop_index('idx_messages_created_at', 'messages')
    op.drop_index('idx_messages_conversation_id', 'messages')
    op.drop_table('messages')

    op.drop_index('idx_conversations_updated_at', 'conversations')
    op.drop_index('idx_conversations_user_id', 'conversations')
    op.drop_table('conversations')
```

---

## Query Patterns

### Common Queries

**1. List user's conversations (most recent first)**
```sql
SELECT * FROM conversations
WHERE user_id = $1
ORDER BY updated_at DESC
LIMIT 20;
```

**2. Get conversation messages (chronological order)**
```sql
SELECT * FROM messages
WHERE conversation_id = $1
ORDER BY created_at ASC;
```

**3. Get recent messages for AI context (last 20)**
```sql
SELECT * FROM messages
WHERE conversation_id = $1
ORDER BY created_at DESC
LIMIT 20;
```

**4. Update conversation timestamp on new message**
```sql
UPDATE conversations
SET updated_at = CURRENT_TIMESTAMP
WHERE id = $1;
```

**5. Count messages in conversation**
```sql
SELECT COUNT(*) FROM messages
WHERE conversation_id = $1;
```

---

## Performance Considerations

### Indexing Strategy

- **Primary Keys**: All tables use UUID primary keys with default generation
- **Foreign Keys**: Indexed for fast joins (user_id, conversation_id)
- **Sorting**: Indexed on created_at and updated_at for chronological ordering
- **Composite Index**: (conversation_id, created_at) for efficient message retrieval

### Query Optimization

- Limit conversation list to recent 20-50 conversations
- Limit message context to recent 20 messages for AI
- Use pagination for older messages
- Consider archiving old conversations (future enhancement)

### Scalability

- UUID primary keys enable distributed ID generation
- Cascade deletes handled by database (efficient)
- Indexes support fast queries even with large datasets
- Stateless backend enables horizontal scaling

---

**Data Model Status**: ✅ Complete
**Next Phase**: API Contracts
