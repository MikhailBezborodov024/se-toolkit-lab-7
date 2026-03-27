# Bot Dockerfile
FROM python:3.14-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy bot files
COPY pyproject.toml uv.lock ./
COPY bot.py ./
COPY config.py ./
COPY handlers/ ./handlers/
COPY services/ ./services/
COPY tools/ ./tools/

# Install dependencies
RUN uv sync --frozen

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:42002/health')" || exit 1

# Run the bot
CMD ["uv", "run", "bot.py"]
