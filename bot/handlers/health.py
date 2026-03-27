"""Handler for /health command."""

from services.lms_client import get_lms_client


def handle_health(user_id: int = 0) -> str:
    """Handle /health command.

    Returns:
        Backend health status with item count
    """
    client = get_lms_client()
    
    # Get items to check if backend is reachable and has data
    items = client.get_items()
    
    if not items:
        return "Backend is DOWN or unreachable"
    
    count = len(items)
    return f"Backend is healthy. {count} items available."
