"""Handler for /labs command."""

from services.lms_client import get_lms_client


def handle_labs(user_id: int = 0) -> str:
    """Handle /labs command.
    
    Returns:
        List of available labs
    """
    client = get_lms_client()
    items = client.get_items()
    
    if not items:
        return "No labs available or backend is unreachable"
    
    # Filter and format labs
    labs = [item for item in items if item.get("type") == "lab"]
    
    if not labs:
        return "No labs found"
    
    result = ["Available labs:"]
    for lab in labs:
        title = lab.get("title", "Unknown")
        result.append(f"  • {title}")
    
    return "\n".join(result)
