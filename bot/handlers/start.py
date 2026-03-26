"""Handler for /start command."""


def handle_start(user_id: int = 0) -> str:
    """Handle /start command.

    Args:
        user_id: The Telegram user ID (unused in placeholder)

    Returns:
        Welcome message text
    """
    return "Welcome! I'm your LMS assistant bot. Use /help to see available commands."
