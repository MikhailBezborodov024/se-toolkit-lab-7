"""Tool definitions for LLM function calling.

Each tool represents a backend API endpoint that the LLM can call.
"""

from services.lms_client import get_lms_client


def get_items_tool() -> dict:
    """Get tool definition for /items/ endpoint."""
    return {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get list of all labs and tasks available in the system. Use this when user asks about available labs, what labs exist, or wants to see the list of labs.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }


def get_learners_tool() -> dict:
    """Get tool definition for /learners/ endpoint."""
    return {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get list of all enrolled students/learners",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }


def get_scores_tool() -> dict:
    """Get tool definition for /analytics/scores endpoint."""
    return {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution (4 buckets) for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier (e.g., 'lab-01', 'lab-04')",
                    },
                },
                "required": ["lab"],
            },
        },
    }


def get_pass_rates_tool() -> dict:
    """Get tool definition for /analytics/pass-rates endpoint."""
    return {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task pass rates (averages) for a specific lab. Use this when user asks about scores, pass rates, or results for a specific lab.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier (e.g., 'lab-01', 'lab-04')",
                    },
                },
                "required": ["lab"],
            },
        },
    }


def get_timeline_tool() -> dict:
    """Get tool definition for /analytics/timeline endpoint."""
    return {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submissions timeline (submissions per day) for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier (e.g., 'lab-01', 'lab-04')",
                    },
                },
                "required": ["lab"],
            },
        },
    }


def get_groups_tool() -> dict:
    """Get tool definition for /analytics/groups endpoint."""
    return {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group performance for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier (e.g., 'lab-01', 'lab-04')",
                    },
                },
                "required": ["lab"],
            },
        },
    }


def get_top_learners_tool() -> dict:
    """Get tool definition for /analytics/top-learners endpoint."""
    return {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get top N learners for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier (e.g., 'lab-01', 'lab-04')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of top learners to return (default: 5)",
                        "default": 5,
                    },
                },
                "required": ["lab"],
            },
        },
    }


def get_completion_rate_tool() -> dict:
    """Get tool definition for /analytics/completion-rate endpoint."""
    return {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get completion percentage for a specific lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {
                        "type": "string",
                        "description": "Lab identifier (e.g., 'lab-01', 'lab-04')",
                    },
                },
                "required": ["lab"],
            },
        },
    }


def sync_pipeline_tool() -> dict:
    """Get tool definition for /pipeline/sync endpoint."""
    return {
        "type": "function",
        "function": {
            "name": "sync_pipeline",
            "description": "Trigger ETL sync to update data from autochecker",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }


def get_all_tools() -> list[dict]:
    """Get all available tool definitions."""
    return [
        get_items_tool(),
        get_learners_tool(),
        get_scores_tool(),
        get_pass_rates_tool(),
        get_timeline_tool(),
        get_groups_tool(),
        get_top_learners_tool(),
        get_completion_rate_tool(),
        sync_pipeline_tool(),
    ]


# Tool execution functions
def execute_get_items() -> str:
    """Execute get_items tool - returns actual lab names."""
    client = get_lms_client()
    items = client.get_items()
    if not items:
        return "No items found or backend is unreachable"
    
    # Extract and format lab names
    labs = [item for item in items if item.get("type") == "lab"]
    if not labs:
        return f"Found {len(items)} items but no labs"
    
    # Format with actual lab titles
    result = ["Available labs:"]
    for lab in labs:
        title = lab.get("title", "Unknown")
        lab_id = lab.get("id", "unknown")
        result.append(f"  • {lab_id}: {title}")
    
    return "\n".join(result)


def execute_get_learners() -> str:
    """Execute get_learners tool."""
    client = get_lms_client()
    # For now, use items count as proxy
    items = client.get_items()
    return f"Found {len(items)} items in the system. Use get_items to see details."


def execute_get_scores(lab: str) -> str:
    """Execute get_scores tool."""
    client = get_lms_client()
    # Note: This endpoint may need to be added to lms_client
    return f"Score distribution for {lab} (endpoint not yet implemented)"


def execute_get_pass_rates(lab: str) -> str:
    """Execute get_pass_rates tool."""
    client = get_lms_client()
    pass_rates = client.get_pass_rates(lab)
    if not pass_rates:
        return f"No pass rates found for {lab}"
    
    result = []
    for entry in pass_rates:
        task = entry.get("task", "Unknown")
        avg = entry.get("avg_score", 0)
        attempts = entry.get("attempts", 0)
        result.append(f"  • {task}: {avg:.1f}% ({attempts} attempts)")
    
    return f"Pass rates for {lab}:\n" + "\n".join(result)


def execute_get_timeline(lab: str) -> str:
    """Execute get_timeline tool."""
    return f"Timeline data for {lab} (endpoint not yet implemented)"


def execute_get_groups(lab: str) -> str:
    """Execute get_groups tool."""
    return f"Group performance for {lab} (endpoint not yet implemented)"


def execute_get_top_learners(lab: str, limit: int = 5) -> str:
    """Execute get_top_learners tool."""
    return f"Top {limit} learners for {lab} (endpoint not yet implemented)"


def execute_get_completion_rate(lab: str) -> str:
    """Execute get_completion_rate tool."""
    return f"Completion rate for {lab} (endpoint not yet implemented)"


def execute_sync_pipeline() -> str:
    """Execute sync_pipeline tool."""
    return "ETL sync triggered (endpoint not yet implemented)"


# Map tool names to execution functions
TOOL_EXECUTORS = {
    "get_items": execute_get_items,
    "get_learners": execute_get_learners,
    "get_scores": execute_get_scores,
    "get_pass_rates": execute_get_pass_rates,
    "get_timeline": execute_get_timeline,
    "get_groups": execute_get_groups,
    "get_top_learners": execute_get_top_learners,
    "get_completion_rate": execute_get_completion_rate,
    "sync_pipeline": execute_sync_pipeline,
}


def execute_tool(tool_name: str, arguments: dict) -> str:
    """Execute a tool by name with given arguments.

    Args:
        tool_name: Name of the tool to execute
        arguments: Arguments to pass to the tool

    Returns:
        Tool execution result as string
    """
    executor = TOOL_EXECUTORS.get(tool_name)
    if not executor:
        return f"Unknown tool: {tool_name}"
    
    try:
        return executor(**arguments)
    except Exception as e:
        return f"Error executing {tool_name}: {str(e)}"
