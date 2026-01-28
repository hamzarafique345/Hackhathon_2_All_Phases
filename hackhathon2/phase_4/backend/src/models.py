"""
SQLModel database models for User, Task, Conversation, and Message entities.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from enum import Enum


class User(SQLModel, table=True):
    """User account model."""

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password_hash: str = Field(max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Task(SQLModel, table=True):
    """Task/todo item model."""

    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Phase 3 AI Chatbot Models

class Conversation(SQLModel, table=True):
    """Conversation model for AI chat sessions."""

    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MessageRole(str, Enum):
    """Message role enum."""
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """Message model for conversation messages."""

    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=50)  # 'user' or 'assistant'
    content: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Pydantic DTOs for API requests/responses

class ConversationCreate(SQLModel):
    """DTO for creating a conversation."""
    title: Optional[str] = None


class ConversationResponse(SQLModel):
    """DTO for conversation response."""
    id: UUID
    user_id: UUID
    title: Optional[str]
    created_at: datetime
    updated_at: datetime


class MessageCreate(SQLModel):
    """DTO for creating a message."""
    role: str  # 'user' or 'assistant'
    content: str


class MessageResponse(SQLModel):
    """DTO for message response."""
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime
