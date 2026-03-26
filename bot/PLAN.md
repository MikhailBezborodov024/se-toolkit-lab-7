# Bot Implementation Plan

## Overview

This document outlines the implementation plan for the LMS Telegram Bot (Lab 7). The bot provides a Telegram interface to the LMS backend, allowing students to check their progress, view labs, and get scores using natural language commands.

## Architecture

The bot follows a layered architecture with clear separation of concerns:

1. **Entry Point (bot.py)**: Main entry point with CLI test mode for testing handlers without Telegram
2. **Handlers (bot/handlers/)**: Pure functions that take input and return text responses
3. **Services (bot/services/)**: External API clients (LMS backend, LLM for intent routing)
4. **Configuration (config.py)**: Environment variable loading and access

## Key Design Decisions

### Handler Separation

Handlers are plain Python functions that don't depend on Telegram. This allows:
- Testing via `--test` mode without Telegram connection
- Unit tests that call handlers directly
- Easy replacement of Telegram with other transport layers

### Test Mode

The `--test` mode parses command strings and routes to handlers directly, printing responses to stdout. This enables quick verification without deploying to Telegram.

### Environment Configuration

Secrets (bot token, API keys) are loaded from `.env.bot.secret` at startup. This file is gitignored to prevent committing secrets.

## Implementation Phases

### Phase 1: Scaffold (Task 1)
- Create bot.py with --test mode
- Create handler directory structure
- Implement placeholder handlers for /start, /help
- Set up pyproject.toml with dependencies

### Phase 2: Backend Integration (Task 2)
- Implement LMS client service
- Add /health handler (calls backend /health endpoint)
- Add /labs handler (calls backend /items/ endpoint)
- Add /scores handler (calls backend /analytics/pass-rates endpoint)
- Handle errors gracefully with user-friendly messages

### Phase 3: LLM Intent Routing (Task 3)
- Implement LLM service for natural language understanding
- Create intent classifier that maps user messages to commands
- Extract parameters from natural language (e.g., "lab-04" from "show me scores for lab 4")
- Handle non-command messages using LLM

### Phase 4: Docker Deployment (Task 4)
- Create Dockerfile for the bot
- Update docker-compose.yml to include bot service
- Configure environment variables for container
- Test deployment and verify bot responds in Telegram

## Testing Strategy

1. **Unit tests**: Test handlers in isolation
2. **Test mode**: Verify commands via `uv run bot.py --test "/command"`
3. **Integration tests**: Test with real backend
4. **E2E tests**: Test in Telegram after deployment

## Acceptance Criteria

- All commands work in --test mode
- Handlers return appropriate responses
- Errors are handled gracefully
- No secrets hardcoded
- Clean separation between handlers and Telegram
