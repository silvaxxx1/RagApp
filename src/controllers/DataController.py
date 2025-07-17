from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSingle

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.scale = 1048576  # 1 MB in bytes

    def validate(self,
                file: UploadFile):
        
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False , ResponseSingle.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * self.scale:
            return False , ResponseSingle.FILE_SIZE_EXCEEDS.value

        return True , ResponseSingle.FILE_UPLOAD_SUCCESS
