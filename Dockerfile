# Multi-stage build for Patchamomma backend

FROM python:3.11-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser
USER appuser

# Cloud Run sets PORT (default 8080); main.py honors it
EXPOSE 8080

# Start application
CMD ["python", "main.py"]
