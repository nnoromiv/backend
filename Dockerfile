# Base image
FROM python:3.12.6

WORKDIR /app

# Install Postgres client (for pg_isready)
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary

# Copy backend code and SQL
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Set entrypoint
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
