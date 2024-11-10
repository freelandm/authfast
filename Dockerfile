# Build stage
FROM python:3.11-slim as builder

# Install poetry
ENV POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip install "poetry==$POETRY_VERSION"

# Set working directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-dev --no-root

# Final stage
FROM python:3.11-slim as runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Set working directory to the project root
WORKDIR /project

# Copy the entire project
COPY . .

# Create non-root user and switch to it
RUN adduser --disabled-password --gecos "" appuser \
    && chown -R appuser:appuser /project
USER appuser

# Expose port
EXPOSE 5000

# Start the application from the project root
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001"]