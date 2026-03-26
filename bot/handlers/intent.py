"""Intent classification handler for natural language queries."""

import re

from services.llm_client import get_llm_client
from services.lms_client import get_lms_client
from tools import get_all_tools, execute_tool


# System prompt for intent classification
SYSTEM_PROMPT = """You are an assistant for a Learning Management System (LMS). 
Your job is to help students get information about their labs, scores, and progress.

You have access to the following tools:
- get_items: Get list of all labs and tasks available - use for "what labs", "list labs", "show labs", "available labs"
- get_learners: Get list of enrolled students
- get_pass_rates: Get per-task pass rates for a specific lab - use for "scores", "pass rates", "results" (requires lab parameter like "lab-04")
- get_scores: Get score distribution (4 buckets) for a specific lab
- get_timeline: Get submissions timeline for a specific lab
- get_groups: Get per-group performance for a specific lab
- get_top_learners: Get top N learners for a specific lab
- get_completion_rate: Get completion percentage for a specific lab
- analyze_pass_rates: Analyze pass rates across all labs to find lowest/highest/average - use for "lowest pass rate", "highest pass rate", "which lab is hardest", "which lab has best scores"
- sync_pipeline: Trigger ETL sync to update data

When a user asks a question, determine which tool to call based on their intent.
If the user mentions a specific lab (like "lab 04", "lab-04", "lab 4"), extract the lab identifier as "lab-XX" format.

Examples:
- "What labs are available?" → get_items
- "Show me scores for lab 04" → get_pass_rates with lab="lab-04"
- "Is the backend working?" → get_items (to check connectivity)
- "How many students are enrolled?" → get_learners
- "Show pass rates for lab 1" → get_pass_rates with lab="lab-01"
- "List all labs" → get_items
- "Which lab has the lowest pass rate?" → analyze_pass_rates with metric="lowest"
- "Which lab is the hardest?" → analyze_pass_rates with metric="lowest"

Always respond in a helpful, concise manner. If you need to call a tool, do so.
If you don't understand the question, suggest using /help for available commands.
"""


def extract_lab_from_query(message: str) -> str | None:
    """Extract lab identifier from user query.
    
    Handles formats like: "lab 04", "lab-04", "lab 4", "lab04"
    Returns: "lab-04" format or None
    """
    # Pattern: lab followed by optional dash and digits
    patterns = [
        r'lab[-\s]?(\d+)',
        r'lab[-\s]?(\d{2})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            num = match.group(1)
            # Ensure 2-digit format
            return f"lab-{num.zfill(2)}"
    
    return None


def handle_intent(message: str) -> str:
    """Handle natural language intent classification.

    Args:
        message: User's natural language message

    Returns:
        Response text from LLM or tool execution result
    """
    llm = get_llm_client()
    tools = get_all_tools()

    # Extract lab if mentioned
    lab = extract_lab_from_query(message)
    
    # Create messages for LLM
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message},
    ]

    # First call: get tool choice from LLM
    response = llm.chat(messages, tools)

    # Check for error
    if "error" in response:
        return f"LLM error: {response['error']}"

    # Check for tool calls
    tool_calls = response.get("tool_calls")
    if tool_calls:
        # Execute the tool
        tool_call = tool_calls[0]
        tool_name = tool_call["function"]["name"]
        
        # Parse arguments
        try:
            arguments = tool_call["function"].get("arguments", "{}")
            if isinstance(arguments, str):
                arguments = eval(arguments)  # Simple parsing for now
        except Exception:
            arguments = {}
        
        # Add extracted lab if not provided
        if lab and "lab" not in arguments:
            arguments["lab"] = lab
        
        # Execute tool
        result = execute_tool(tool_name, arguments)
        
        # Format response
        return result

    # No tool call - return LLM's direct response
    content = response.get("content", "I'm not sure how to help with that. Try /help for available commands.")
    return content
