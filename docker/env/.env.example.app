# ========================= App Info =========================
APP_NAME="RagApp"
APP_VERSION="0.1"

# ========================= File Handling =====================
FILE_ALLOWED_TYPES=["text/plain", "application/pdf"]
FILE_MAX_SIZE=10
FILE_DEFAULT_CHUNK_SIZE=512000  # 512KB

# ========================= Postgres Config ==================
POSTGRES_USERNAME="postgres"
POSTGRES_PASSWORD="raggapp_postgres123"
POSTGRES_HOST="pgvector" 
POSTGRES_PORT=5432
POSTGRES_MAIN_DATABASE="RagApp"

# ========================= LLM Config =======================
GENERATION_BACKEND="openai"
EMBEDDING_BACKEND="open_source_embeddings"

OPENAI_API_KEY="your_openai_api_key_here"
OPENAI_API_URL="https://6f6ee03ddfdf.ngrok-free.app/v1/"
COHERE_API_KEY="your_cohere_api_key_here"

GENERATION_MODEL_ID_LITERAL = ["gpt-4o-mini", "gpt-4o", "gemma2:9b-instruct-q5_0"]
GENERATION_MODEL_ID="gemma2:9b-instruct-q5_0"
EMBEDDING_MODEL_ID="intfloat/e5-large-v2"
EMBEDDING_MODEL_SIZE=1024

# ⚠ Keep typo to match your factoryR
INPUT_DAFAULT_MAX_CHARACTERS=1024
GENERATION_DAFAULT_MAX_TOKENS=200
GENERATION_DAFAULT_TEMPERATURE=0.1

# ================== Vector DB Config ========================
VECTOR_DB_BACKEND_LITERAL = ["QDRANT","PGVECTOR"]
VECTOR_DB_BACKEND="PGVECTOR"
VECTOR_DB_PATH="qdrant_db"
VECTOR_DB_METHOD="cosine"  # used internally by factory
VECTOR_DB_PGVEC_INDEX_THRESHOLD = 200

# ======================== Template Config ==================
DEFAULT_LANG="en"
PRIMARY_LANG="en"
