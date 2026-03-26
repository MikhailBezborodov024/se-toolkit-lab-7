"""Handler for /scores command."""

from services.lms_client import get_lms_client


def handle_scores(user_id: int = 0, lab: str = "") -> str:
    """Handle /scores command.

    Args:
        user_id: The Telegram user ID
        lab: Lab identifier (e.g., "lab-04")

    Returns:
        Score information for the specified lab
    """
    if not lab:
        return "Usage: /scores <lab> (e.g., /scores lab-04)"

    client = get_lms_client()
    pass_rates = client.get_pass_rates(lab)

    if not pass_rates:
        return f"No pass rates found for '{lab}' or backend is unreachable"

    # Format pass rates - the API returns [{"task": "...", "avg_score": ..., "attempts": ...}]
    result = [f"Pass rates for {lab}:"]
    
    for entry in pass_rates:
        task_name = entry.get("task", "Unknown")
        avg_score = entry.get("avg_score", 0)
        attempts = entry.get("attempts", 0)
        # avg_score is already a percentage (0-100)
        result.append(f"  • {task_name}: {avg_score:.1f}% ({attempts} attempts)")

    return "\n".join(result)
