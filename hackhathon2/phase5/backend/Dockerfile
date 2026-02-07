# Backend Dockerfile for FastAPI Todo Chatbot
# Multi-folder Python application with proper PYTHONPATH configuration

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire backend directory structure
# This includes: src/, ai_agent/, tests/
COPY . .

# Set PYTHONPATH to enable imports like "from src.database import..."
ENV PYTHONPATH=/app

# Expose port 8000
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run uvicorn server
# --host 0.0.0.0 is required for container networking
# --port 8000 matches the exposed port
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
