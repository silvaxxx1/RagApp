from enum import Enum 



class VectorDBEnums(Enum):
    QDRANT = "QDRANT" 
    PGVECTOR = "PGVECTOR"

class DistanceMethodEnums(Enum):
    COSINE = "cosine"
    DOT = "dot" 

class pgVectorTableSchemeEnums(Enum):
    ID = "id"
    TEXT = "text"
    VECTOR = "vector"
    CHUNK_ID = "chunk_id"
    METADATA = "metadata"
    _PREFIX = "pgvector" 

class pgVectorDistanceMethodEnums(Enum):
    COSINE = "vector_cosine_ops"
    DOT = "vector_l2_ops" 

class pgVectorIndexTypeEnums(Enum):
    HNSW = "hnsw" 
    IVFFLAT = "ivfflat"
     
