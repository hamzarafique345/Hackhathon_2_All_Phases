"use client";

import { useState, useCallback, useEffect } from "react";
import { chatService, type Message } from "@/lib/chatService";
import { useAuth } from "@/components/auth/AuthContext";

export function useChat() {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Create a new conversation when component mounts
  useEffect(() => {
    if (user?.id && !conversationId) {
      createNewConversation();
    }
  }, [user?.id]);

  const createNewConversation = async () => {
    if (!user?.id) return;

    try {
      const conversation = await chatService.createConversation(user.id);
      setConversationId(conversation.id);
    } catch (error) {
      console.error("Error creating conversation:", error);
      setError("Failed to create conversation");
    }
  };

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim() || !user?.id || !conversationId) return;

      setIsLoading(true);
      setError(null);

      try {
        // Add user message to UI immediately
        const tempUserMessage: Message = {
          id: `temp-user-${Date.now()}`,
          conversation_id: conversationId,
          role: "user",
          content,
          created_at: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, tempUserMessage]);

        // Send message to backend (which will trigger AI response)
        const aiResponse = await chatService.createMessage(
          user.id,
          conversationId,
          {
            role: "user",
            content,
          }
        );

        // Replace temp message with actual messages from backend
        // The backend returns the AI response, so we need to fetch all messages
        const allMessages = await chatService.getMessages(
          user.id,
          conversationId
        );
        setMessages(allMessages);
      } catch (error: any) {
        console.error("Error sending message:", error);
        setError(
          error.response?.data?.detail || "Failed to send message. Please try again."
        );
        // Remove the temporary message on error
        setMessages((prev) =>
          prev.filter((msg) => !msg.id.startsWith("temp-"))
        );
      } finally {
        setIsLoading(false);
      }
    },
    [user?.id, conversationId]
  );

  const loadConversation = async (convId: string) => {
    if (!user?.id) return;

    try {
      setIsLoading(true);
      const messages = await chatService.getMessages(user.id, convId);
      setMessages(messages);
      setConversationId(convId);
    } catch (error) {
      console.error("Error loading conversation:", error);
      setError("Failed to load conversation");
    } finally {
      setIsLoading(false);
    }
  };

  return {
    messages,
    sendMessage,
    isLoading,
    conversationId,
    error,
    loadConversation,
    createNewConversation,
  };
}
