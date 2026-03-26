"""Handler for /help command."""


def handle_help(user_id: int = 0) -> str:
    """Handle /help command.
    
    Returns:
        List of available commands
    """
    return (
        "Available commands:\n"
        "  /start - Welcome message\n"
        "  /help - Show this help message\n"
        "  /health - Check backend status\n"
        "  /labs - List available labs\n"
        "  /scores <lab> - Get scores for a specific lab"
    )
