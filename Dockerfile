# Use a Linux-compatible Python version
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for pythonnet and Postgres client
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt .

# Remove Windows-only packages (pywin32, pypiwin32) before installing
RUN sed -i '/pywin32/d' requirements.txt && sed -i '/pypiwin32/d' requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code and SQL files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set entrypoint
ENTRYPOINT ["./entrypoint.sh"]
