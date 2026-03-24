# LMS Telegram Bot — Development Plan

## Overview

This document outlines the development plan for building a Telegram bot that integrates with the LMS backend. The bot allows users to check system health, browse labs and scores, and ask questions in plain language using an LLM for intent classification.

## Task 1: Plan and Scaffold

**Goal:** Establish the project structure and testable handler architecture.

**Approach:**
- Create `bot/` directory with `bot.py` as the entry point
- Implement `--test` mode for CLI testing without Telegram connection
- Separate handlers into `bot/handlers/` directory — these are plain functions that don't depend on Telegram
- Create `bot/config.py` for environment variable loading from `.env.bot.secret`
- Create `bot/services/` directory for future API clients

**Key Pattern:** Testable handlers — the same handler functions work from `--test` mode, unit tests, or Telegram. This is *separation of concerns*.

## Task 2: Backend Integration

**Goal:** Implement slash commands that fetch real data from the LMS backend.

**Approach:**
- Create `bot/services/lms_client.py` — an API client that wraps HTTP calls to the backend
- Implement Bearer token authentication using `LMS_API_KEY`
- Update handlers: `/health` (check backend status), `/labs` (list items), `/scores <lab>` (get analytics)
- Add error handling for backend failures (friendly messages, no crashes)

**Key Pattern:** API client abstraction — handlers call the client, not raw HTTP. This makes testing easier and centralizes error handling.

## Task 3: Intent-Based Natural Language Routing

**Goal:** Allow users to send plain text messages that the bot interprets using an LLM.

**Approach:**
- Create `bot/services/llm_service.py` — integrates with Qwen LLM API
- Implement intent classification: map natural language to commands (e.g., "check my scores" → `/scores`)
- Extract parameters from user input (e.g., "lab-04" from "what are my scores for lab 4?")
- Add message handler for non-command messages in Telegram mode

**Key Pattern:** LLM tool use — the LLM reads tool descriptions to decide which API to call. Description quality matters more than prompt engineering.

## Task 4: Containerize and Deploy

**Goal:** Deploy the bot alongside the backend using Docker Compose.

**Approach:**
- Create `bot/Dockerfile` — Python 3.12-slim base, uv installed, entry point configured
- Update `docker-compose.yml` — add bot service, link with backend using service names (not localhost)
- Create `.env.bot.secret` on VM with `BOT_TOKEN`, `LLM_API_KEY`, `BACKEND_URL`
- Test deployment and verify bot responds in Telegram
- Update README with deployment instructions

**Key Pattern:** Docker networking — containers communicate via service names (e.g., `backend`), not `localhost`.

## Testing Strategy

- **Unit tests:** Test handlers in isolation (future work)
- **CLI test mode:** `uv run bot.py --test "/command"` for quick verification
- **Integration tests:** Deploy to VM and test in Telegram

## Git Workflow

For each task:
1. Create GitHub issue
2. Create feature branch: `feature/lab7-task-X`
3. Implement, test, commit locally
4. Push and create PR on GitHub
5. Partner review, then merge
