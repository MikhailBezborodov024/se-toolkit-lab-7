"""Configuration loading from environment variables."""

import os
from pathlib import Path


def load_env() -> None:
    """Load environment variables from .env.bot.secret if it exists.
    
    This function reads the .env.bot.secret file in the bot directory
    and sets environment variables for use by the application.
    """
    env_path = Path(__file__).parent / ".env.bot.secret"
    
    if not env_path.exists():
        return
    
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            # Parse KEY=VALUE
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                # Only set if not already in environment
                if key not in os.environ:
                    os.environ[key] = value


def get_bot_token() -> str:
    """Get the Telegram bot token."""
    return os.environ.get("BOT_TOKEN", "")


def get_lms_api_base_url() -> str:
    """Get the LMS API base URL."""
    return os.environ.get("LMS_API_BASE_URL", "http://localhost:42002")


def get_lms_api_key() -> str:
    """Get the LMS API key."""
    return os.environ.get("LMS_API_KEY", "")


def get_llm_api_key() -> str:
    """Get the LLM API key."""
    return os.environ.get("LLM_API_KEY", "")


def get_llm_api_base_url() -> str:
    """Get the LLM API base URL."""
    return os.environ.get("LLM_API_BASE_URL", "")


def get_llm_api_model() -> str:
    """Get the LLM API model name."""
    return os.environ.get("LLM_API_MODEL", "coder-model")
