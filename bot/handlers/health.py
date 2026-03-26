"""Handler for /health command."""

from services.lms_client import get_lms_client


def handle_health(user_id: int = 0) -> str:
    """Handle /health command.

    Returns:
        Backend health status with item count
    """
    client = get_lms_client()
    
    # First check if backend is reachable
    is_healthy = client.health_check()
    if not is_healthy:
        return "Backend is DOWN or unreachable"
    
    # Get items count to prove backend has data
    items = client.get_items()
    count = len(items) if items else 0
    
    return f"Backend is healthy. {count} items available."
