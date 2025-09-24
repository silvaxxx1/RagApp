FROM ghcr.io/astral-sh/uv:0.6.14-python3.10-bookworm

WORKDIR /app

# Install system dependencies including postgresql-client
RUN apt-get update && apt-get install -y \
    build-essential \
    libavif-dev pkg-config \
    libjpeg-dev \
    gcc unzip zip \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    curl \
    postgresql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY src/requirements.txt .
RUN uv pip install -r requirements.txt --system

# Copy application source
COPY src/ .

# Create directory structure for Alembic
RUN mkdir -p /app/models/db_schemes/RagApp/
COPY docker/RagApp/alembic.ini /app/models/db_schemes/RagApp/alembic.ini

# Copy and set entrypoint
COPY docker/RagApp/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Command to run the application (default)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
