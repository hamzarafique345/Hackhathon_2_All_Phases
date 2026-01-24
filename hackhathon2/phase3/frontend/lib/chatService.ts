/**
 * Chat service for conversation and message API calls.
 */
import apiClient from "./api-client";

export interface Conversation {
  id: string;
  user_id: string;
  title: string | null;
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: string;
  conversation_id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export interface CreateConversationRequest {
  title?: string;
}

export interface CreateMessageRequest {
  role: "user" | "assistant";
  content: string;
}

class ChatService {
  /**
   * Create a new conversation
   */
  async createConversation(
    userId: string,
    data: CreateConversationRequest = {}
  ): Promise<Conversation> {
    const response = await apiClient.post(
      `/api/users/${userId}/conversations`,
      data
    );
    return response.data;
  }

  /**
   * List all conversations for a user
   */
  async listConversations(
    userId: string,
    limit: number = 20,
    offset: number = 0
  ): Promise<Conversation[]> {
    const response = await apiClient.get(`/api/users/${userId}/conversations`, {
      params: { limit, offset },
    });
    return response.data;
  }

  /**
   * Get a specific conversation
   */
  async getConversation(
    userId: string,
    conversationId: string
  ): Promise<Conversation> {
    const response = await apiClient.get(
      `/api/users/${userId}/conversations/${conversationId}`
    );
    return response.data;
  }

  /**
   * Get messages for a conversation
   */
  async getMessages(
    userId: string,
    conversationId: string,
    limit: number = 50,
    offset: number = 0
  ): Promise<Message[]> {
    const response = await apiClient.get(
      `/api/users/${userId}/conversations/${conversationId}/messages`,
      { params: { limit, offset } }
    );
    return response.data;
  }

  /**
   * Create a new message in a conversation
   */
  async createMessage(
    userId: string,
    conversationId: string,
    data: CreateMessageRequest
  ): Promise<Message> {
    const response = await apiClient.post(
      `/api/users/${userId}/conversations/${conversationId}/messages`,
      data
    );
    return response.data;
  }

  /**
   * Delete a conversation
   */
  async deleteConversation(
    userId: string,
    conversationId: string
  ): Promise<void> {
    await apiClient.delete(
      `/api/users/${userId}/conversations/${conversationId}`
    );
  }
}

export const chatService = new ChatService();
