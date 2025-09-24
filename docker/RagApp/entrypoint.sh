#!/bin/bash
set -e

# Wait for Postgres to be ready
echo "Waiting for Postgres..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USERNAME"; do
  sleep 2
done

# Run migrations once
echo "Running database migrations..."
cd /app/models/db_schemes/RagApp/
alembic upgrade head
cd /app

# Start FastAPI
echo "Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
