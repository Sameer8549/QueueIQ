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
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and code
COPY queueiq-backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY queueiq-backend/ .

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
