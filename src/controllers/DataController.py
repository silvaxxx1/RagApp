from .BaseController import BaseController
from fastapi import UploadFile
class DataController(BaseController):
    def __init__(self):
       super().__init__() 
       self.scale = 1048576

    def validate(self, file: UploadFile):
        if file.content_type not in self.app_settings.ALLOWED_FILE_TYPES:
            return False , "Invalid file type" 
        
        if file.size > self.app_settings.MAX_FILE_SIZE * self.scale:
            return False , "File size too large" 
        
        return True
        



