#!/usr/bin/env python3
"""
Telegram bot entry point with CLI test mode.

Usage:
    uv run bot.py --test "/command"    # Test mode (no Telegram connection)
    uv run bot.py                       # Normal mode (connects to Telegram)
"""

import argparse
import sys

from config import load_env
from handlers import (
    handle_start,
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
)

# Load environment variables at startup
load_env()


def run_test_mode(command: str) -> None:
    """Run a command in test mode and print result to stdout.

    Args:
        command: The command string (e.g., "/start", "/scores lab-04")
    """
    # Parse command and arguments
    parts = command.strip().split(maxsplit=1)
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else ""

    # Route to appropriate handler
    if cmd == "/start":
        response = handle_start()
    elif cmd == "/help":
        response = handle_help()
    elif cmd == "/health":
        response = handle_health()
    elif cmd == "/labs":
        response = handle_labs()
    elif cmd == "/scores":
        response = handle_scores(lab=arg)
    else:
        response = f"Unknown command: {cmd}. Use /help for available commands."

    # Print to stdout and exit cleanly
    print(response)
    sys.exit(0)


def run_normal_mode() -> None:
    """Run the bot in normal Telegram mode."""
    print("Normal mode not implemented yet", file=sys.stderr)
    sys.exit(1)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument(
        "--test",
        type=str,
        metavar="COMMAND",
        help="Run in test mode with the given command (e.g., '/start')"
    )

    args = parser.parse_args()

    if args.test:
        run_test_mode(args.test)
    else:
        run_normal_mode()


if __name__ == "__main__":
    main()
