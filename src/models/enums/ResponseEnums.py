from enum import Enum 


class ResponseSingle(Enum):

    FILE_TYPE_NOT_SUPPORTED = "file_type_not_supported"
    FILE_TYPE_SUCCESS = "file_type_success"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_error"
    FILE_SIZE_EXCEEDS = "file_size_exceeds"
    PROCESSING_SUCCESS = "processing_success"
    PROCESSING_FAILED = "processing_failed"
    NO_FILE_ERROR = "no_file_found"
    FILE_ID_ERROR = "no_file_found_with_this_id"
    PROJECT_NOT_FOUND = "project_not_found"
    INSERT_INTO_VECTOR_DB_ERROR = "insert_into_vector_db_failed"
    INSERT_INTO_VECTOR_DB_SUCCESS = "insert_into_vector_db_success"
    VECTORDB_COLLECTION_RETRIEVED = "vector_db_collection_retrieved"
    VECTORDB_SEARCH_SUCCESS = "vector_db_search_success"
    VECTORDB_SEARCH_ERROR = "vector_db_search_failed"
    RAG_ANSWER_SUCCESS = "rag_answer_success"
    RAG_ANSWER_FAILED = "rag_answer_failed"
