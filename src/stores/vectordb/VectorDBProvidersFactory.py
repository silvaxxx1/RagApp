# src/stores/VectorDBProviderFactory.py

import os
from .providers import QdrantDBProvider, PGVectorProvider
from .VectorDBEnums import VectorDBEnums
from controllers.BaseController import BaseController
from sqlalchemy.orm import sessionmaker

class VectorDBProviderFactory:
    def __init__(self, db_client: sessionmaker = None):
        self.base_controller = BaseController()
        self.db_client = db_client

        # Read config from environment or provide defaults
        self.vector_db_backend = os.getenv("VECTOR_DB_BACKEND", "QDRANT")
        self.vector_db_path = os.getenv("VECTOR_DB_PATH", "qdrant_db")
        self.vector_db_method = os.getenv("VECTOR_DB_METHOD", "cosine")
        self.embedding_model_size = int(os.getenv("EMBEDDING_MODEL_SIZE", 1024))
        self.vector_db_pg_index_threshold = int(os.getenv("VECTOR_DB_PGVEC_INDEX_THRESHOLD", 100))

    def create(self, provider: str):
        provider_upper = provider.upper()

        if provider_upper == VectorDBEnums.QDRANT.value:
            qdrant_db_client = self.base_controller.get_database_path(db_name=self.vector_db_path)

            return QdrantDBProvider(
                db_client=qdrant_db_client,
                distance_method=self.vector_db_method,
                default_vector_size=self.embedding_model_size,
                index_threshold=self.vector_db_pg_index_threshold,
            )

        if provider_upper == VectorDBEnums.PGVECTOR.value:
            return PGVectorProvider(
                db_client=self.db_client,
                distance_method=self.vector_db_method,
                default_vector_size=self.embedding_model_size,
                index_threshold=self.vector_db_pg_index_threshold,
            )

        return None
