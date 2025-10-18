#!/bin/bash
set -e

echo "🚀 Starting backend on Cloud Run..."

# Database initialization (if needed)
echo "⏳ Initializing database tables..."
python init_db.py
echo "✅ Database initialization complete!"

# Start FastAPI on the port provided by Cloud Run
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
