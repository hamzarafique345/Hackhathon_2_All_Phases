"""
OpenRouter API configuration for AI agent.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class OpenRouterConfig:
    """Configuration for OpenRouter API."""

    def __init__(self):
        """Initialize OpenRouter configuration."""
        self.api_key: Optional[str] = os.getenv("OPENROUTER_API_KEY")
        self.api_base_url: str = "https://openrouter.ai/api/v1"
        self.model: str = "meta-llama/llama-3.2-3b-instruct:free"
        self.api_base: str = os.getenv("API_BASE_URL", "http://localhost:8000")

        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY environment variable is not set. "
                "Please add it to your .env file."
            )

    def get_headers(self) -> dict:
        """Get HTTP headers for OpenRouter API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:3000",  # Optional, for rankings
            "X-Title": "AI Todo Chatbot",  # Optional, for rankings
        }

    def get_model_config(self) -> dict:
        """Get model configuration for OpenSDK."""
        return {
            "model": self.model,
            "provider": "openrouter",
            "api_key": self.api_key,
            "base_url": self.api_base_url,
        }


# Global config instance
config = OpenRouterConfig()
