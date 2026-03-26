"""
Command handlers for the LMS Telegram bot.

Handlers are plain functions that take input and return text.
They don't depend on Telegram — same logic works from:
- CLI test mode (--test)
- Unit tests
- Telegram bot
"""

from .start import handle_start
from .help import handle_help
from .health import handle_health
from .labs import handle_labs
from .scores import handle_scores

__all__ = [
    "handle_start",
    "handle_help",
    "handle_health",
    "handle_labs",
    "handle_scores",
]
