#!/bin/bash
set -e

echo "⏳ Waiting for Postgres to be ready..."

# Wait until Postgres is ready
until pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
  echo "Waiting for Postgres at $POSTGRES_HOST:$POSTGRES_PORT..."
  sleep 2
done

echo "✅ Postgres is ready!"

# Run database initialization
echo "⏳ Initializing database tables..."
python init_db.py
echo "✅ Database initialization complete!"

# Start FastAPI
echo "🚀 Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port "${PORT:-8080}"
