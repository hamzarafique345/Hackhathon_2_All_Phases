"""
Conversation API endpoints for Phase 3 AI chatbot.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from ..database import get_session
from ..models import (
    ConversationCreate,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)
from ..services.conversation_service import ConversationService
from ..auth import get_current_user, security

# Import AI agent
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_agent.agent import get_agent

router = APIRouter()


@router.post("/api/users/{user_id}/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    user_id: UUID,
    data: ConversationCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
):
    """Create a new conversation for the user."""
    # Verify user_id matches authenticated user
    if str(current_user["sub"]) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in URL does not match authenticated user",
        )

    # Create conversation
    conversation = await ConversationService.create_conversation(
        session, user_id, data
    )
    return conversation


@router.get("/api/users/{user_id}/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    user_id: UUID,
    limit: int = 20,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
):
    """List all conversations for the user."""
    # Verify user_id matches authenticated user
    if str(current_user["sub"]) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in URL does not match authenticated user",
        )

    # Get conversations
    conversations = await ConversationService.get_conversations(
        session, user_id, limit, offset
    )
    return conversations


@router.get("/api/users/{user_id}/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    user_id: UUID,
    conversation_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
):
    """Get a specific conversation."""
    # Verify user_id matches authenticated user
    if str(current_user["sub"]) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in URL does not match authenticated user",
        )

    # Get conversation
    conversation = await ConversationService.get_conversation(
        session, conversation_id, user_id
    )

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return conversation


@router.get("/api/users/{user_id}/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    user_id: UUID,
    conversation_id: UUID,
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
):
    """Get messages for a conversation."""
    # Verify user_id matches authenticated user
    if str(current_user["sub"]) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in URL does not match authenticated user",
        )

    # Get messages
    messages = await ConversationService.get_messages(
        session, conversation_id, user_id, limit, offset
    )

    if messages is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return messages


@router.post("/api/users/{user_id}/conversations/{conversation_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    user_id: UUID,
    conversation_id: UUID,
    data: MessageCreate,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    Create a new message in a conversation.
    If the message is from a user, invoke the AI agent to generate a response.
    """
    # Verify user_id matches authenticated user
    if str(current_user["sub"]) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in URL does not match authenticated user",
        )

    # Create user message
    user_message = await ConversationService.create_message(
        session, conversation_id, user_id, data
    )

    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    # If message is from user, invoke AI agent to generate response
    if data.role == "user":
        try:
            # Get conversation history
            messages = await ConversationService.get_messages(
                session, conversation_id, user_id, limit=20
            )

            # Format conversation history for AI
            conversation_history = [
                {"role": msg.role, "content": msg.content}
                for msg in (messages or [])
            ]

            # Get JWT token from Authorization header
            jwt_token = credentials.credentials

            # Invoke AI agent
            agent = get_agent()
            ai_response = await agent.process_message(
                message=data.content,
                conversation_history=conversation_history,
                jwt_token=jwt_token,
            )

            # Create AI response message
            ai_message_data = MessageCreate(
                role="assistant",
                content=ai_response,
            )

            ai_message = await ConversationService.create_message(
                session, conversation_id, user_id, ai_message_data
            )

            # Return the AI response message
            return ai_message

        except Exception as e:
            # If AI processing fails, still return the user message
            # Log the error for debugging
            print(f"AI agent error: {str(e)}")
            return user_message

    # If message is from assistant, just return it
    return user_message


@router.delete("/api/users/{user_id}/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    user_id: UUID,
    conversation_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user = Depends(get_current_user),
):
    """Delete a conversation and all its messages."""
    # Verify user_id matches authenticated user
    if str(current_user["sub"]) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in URL does not match authenticated user",
        )

    # Delete conversation
    deleted = await ConversationService.delete_conversation(
        session, conversation_id, user_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return None
