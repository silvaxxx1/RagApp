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