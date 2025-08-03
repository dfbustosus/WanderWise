# syntax=docker/dockerfile:1
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY .env.example .

# Set permissions
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Entrypoint for production
CMD ["python", "-m", "uvicorn", "wanderwise.main:app", "--host", "0.0.0.0", "--port", "8000"]

# For development, override CMD with: 
# CMD ["python", "-m", "uvicorn", "wanderwise.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
