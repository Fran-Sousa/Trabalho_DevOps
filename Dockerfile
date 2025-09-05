# Multi-stage Dockerfile for FastAPI application
# Supports dev, production, and test environments

# Base stage with common dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.5.1 \
    COVERAGE_FILE=/tmp/.coverage

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user with matching host UID
RUN useradd --create-home --shell /bin/bash --uid 1000 app

# Copy requirements for better caching
COPY requirements.txt .
COPY requirements-dev.txt .

# Development stage
FROM base as development

# Install development dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy application code and config files
COPY --chown=app:app . .
COPY --chown=app:app .pre-commit-config.yaml .

# Switch to non-root user
USER app

# Install pre-commit hooks
RUN pre-commit install --install-hooks || true

# Expose port
EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Development command with hot reload
CMD ["fastapi", "dev", "src/main.py", "--host", "0.0.0.0", "--port", "8001"]

# Test stage
FROM development as test

# Switch back to root for installing test dependencies
USER root

# Install additional test dependencies if needed
RUN pip install --no-cache-dir \
    pytest-asyncio \
    httpx \
    pytest-mock

# Copy test files
COPY --chown=app:app tests/ tests/

# Switch to non-root user
USER app

# Run tests by default
CMD ["pytest", "tests/", "-v", "--cov=src", "--cov-report=term-missing"]

# Production stage
FROM base as production

# Install only production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=app:app src/ src/
COPY --chown=app:app pyproject.toml .
COPY --chown=app:app migrate.py .
COPY --chown=app:app entrypoint.sh .
COPY --chown=app:app alembic.ini .
COPY --chown=app:app migrations/ migrations/

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Production command
CMD ["fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]