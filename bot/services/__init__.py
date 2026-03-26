"""Services for the Telegram bot."""

from .lms_client import get_lms_client, LMSClient

__all__ = ["get_lms_client", "LMSClient"]
