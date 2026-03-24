"""
Services for the LMS Telegram bot.

Services handle external dependencies:
- LMS API client (for fetching labs, scores, etc.)
- LLM client (for intent classification in Task 3)
"""

from .lms_client import LMSClient, get_lms_client

__all__ = ["LMSClient", "get_lms_client"]
