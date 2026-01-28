"""
Conversation service for managing AI chat conversations and messages.
"""
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlmodel import col

from ..models import (
    Conversation,
    Message,
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)


class ConversationService:
    """Service for conversation and message operations."""

    @staticmethod
    async def create_conversation(
        session: AsyncSession, user_id: UUID, data: ConversationCreate
    ) -> ConversationResponse:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=user_id,
            title=data.title,
        )
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

        return ConversationResponse(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
        )

    @staticmethod
    async def get_conversations(
        session: AsyncSession, user_id: UUID, limit: int = 20, offset: int = 0
    ) -> List[ConversationResponse]:
        """Get all conversations for a user."""
        result = await session.execute(
            select(Conversation)
            .where(col(Conversation.user_id) == user_id)
            .order_by(col(Conversation.updated_at).desc())
            .limit(limit)
            .offset(offset)
        )
        conversations = result.scalars().all()

        return [
            ConversationResponse(
                id=conv.id,
                user_id=conv.user_id,
                title=conv.title,
                created_at=conv.created_at,
                updated_at=conv.updated_at,
            )
            for conv in conversations
        ]

    @staticmethod
    async def get_conversation(
        session: AsyncSession, conversation_id: UUID, user_id: UUID
    ) -> Optional[ConversationResponse]:
        """Get a specific conversation."""
        result = await session.execute(
            select(Conversation).where(
                col(Conversation.id) == conversation_id,
                col(Conversation.user_id) == user_id,
            )
        )
        conversation = result.scalar_one_or_none()

        if not conversation:
            return None

        return ConversationResponse(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
        )

    @staticmethod
    async def create_message(
        session: AsyncSession,
        conversation_id: UUID,
        user_id: UUID,
        data: MessageCreate,
    ) -> Optional[MessageResponse]:
        """Create a new message in a conversation."""
        # Verify conversation exists and belongs to user
        result = await session.execute(
            select(Conversation).where(
                col(Conversation.id) == conversation_id,
                col(Conversation.user_id) == user_id,
            )
        )
        conversation = result.scalar_one_or_none()

        if not conversation:
            return None

        # Create message
        message = Message(
            conversation_id=conversation_id,
            role=data.role,
            content=data.content,
        )
        session.add(message)

        # Update conversation updated_at timestamp
        await session.execute(
            update(Conversation)
            .where(col(Conversation.id) == conversation_id)
            .values(updated_at=datetime.utcnow())
        )

        await session.commit()
        await session.refresh(message)

        return MessageResponse(
            id=message.id,
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
        )

    @staticmethod
    async def get_messages(
        session: AsyncSession,
        conversation_id: UUID,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> Optional[List[MessageResponse]]:
        """Get messages for a conversation."""
        # Verify conversation exists and belongs to user
        result = await session.execute(
            select(Conversation).where(
                col(Conversation.id) == conversation_id,
                col(Conversation.user_id) == user_id,
            )
        )
        conversation = result.scalar_one_or_none()

        if not conversation:
            return None

        # Get messages
        result = await session.execute(
            select(Message)
            .where(col(Message.conversation_id) == conversation_id)
            .order_by(col(Message.created_at).asc())
            .limit(limit)
            .offset(offset)
        )
        messages = result.scalars().all()

        return [
            MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at,
            )
            for msg in messages
        ]

    @staticmethod
    async def delete_conversation(
        session: AsyncSession, conversation_id: UUID, user_id: UUID
    ) -> bool:
        """Delete a conversation and all its messages."""
        result = await session.execute(
            select(Conversation).where(
                col(Conversation.id) == conversation_id,
                col(Conversation.user_id) == user_id,
            )
        )
        conversation = result.scalar_one_or_none()

        if not conversation:
            return False

        await session.delete(conversation)
        await session.commit()
        return True
