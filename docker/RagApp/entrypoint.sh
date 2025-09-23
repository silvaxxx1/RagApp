#!/bin/bash
set -e

# ========================
# Run database migrations
# ========================
echo "🚀 Running DB migration..."
cd /app/models/db_schemes/RagApp/
alembic upgrade head
cd /app

# ========================
# Start FastAPI server
# ========================
echo "🚀 Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
