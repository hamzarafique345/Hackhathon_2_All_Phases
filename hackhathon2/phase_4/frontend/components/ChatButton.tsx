"use client";

import { MessageSquare } from "lucide-react";
import { Button } from "./ui/button";

interface ChatButtonProps {
  onClick: () => void;
  isOpen: boolean;
}

export function ChatButton({ onClick, isOpen }: ChatButtonProps) {
  return (
    <Button
      onClick={onClick}
      className="fixed bottom-6 right-6 h-14 w-14 rounded-full shadow-lg hover:shadow-xl transition-all z-50"
      size="icon"
      aria-label={isOpen ? "Close chat" : "Open chat"}
    >
      <MessageSquare className="h-6 w-6" />
    </Button>
  );
}
