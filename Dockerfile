# This is the root-level Dockerfile for the QueueIQ Monorepo.
# To deploy a specific service, it is recommended to set the "Root Directory" 
# or "Dockerfile Path" in your deployment platform settings.

# Defaulting to the Backend Service for root-level builds
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install build tools
RUN pip install --no-cache-dir wheel setuptools

# Copy backend requirements and code
COPY queueiq-backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY queueiq-backend/ .

# Expose port 8000
EXPOSE 8000

# Run the application
# Use shell form to allow environment variable expansion
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
