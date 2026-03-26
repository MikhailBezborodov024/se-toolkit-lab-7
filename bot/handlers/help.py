"""Handler for /help command."""


def handle_help(user_id: int = 0) -> str:
    """Handle /help command.

    Args:
        user_id: The Telegram user ID (unused)

    Returns:
        List of available commands with descriptions
    """
    commands = [
        "/start - Welcome message",
        "/help - Show this help message",
        "/health - Check backend status",
        "/labs - List available labs",
        "/scores <lab> - Show pass rates for a lab",
    ]
    return "Available commands:\n" + "\n".join(f"  {cmd}" for cmd in commands)
