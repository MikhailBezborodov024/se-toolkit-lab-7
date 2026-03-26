"""Handler for /health command."""

from services.lms_client import get_lms_client


def handle_health(user_id: int = 0) -> str:
    """Handle /health command.
    
    Returns:
        Backend health status
    """
    client = get_lms_client()
    is_healthy = client.health_check()
    
    if is_healthy:
        return "Backend is UP and running"
    else:
        return "Backend is DOWN or unreachable"
