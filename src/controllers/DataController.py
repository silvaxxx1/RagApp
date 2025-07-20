from .BaseController import BaseController
from .ProjectController import ProjectController    
from fastapi import UploadFile
from models import ResponseSingle
import re
import os

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

    def generate_filepath(self,
                          org_filename: str,
                          project_id: str):
        
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)

        clean_filename = self.get_clean_filename(
                        org_filename=org_filename)
        
        new_file_path = os.path.join(project_path,
                                    random_key+"_"+clean_filename)

        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_path,
                                        random_key+"_"+clean_filename)

        return new_file_path , random_key

    def get_clean_filename(self,
                           org_filename: str):
        
        clean_filename = re.sub(r'[^\w\.]', '', org_filename.strip())
        clean_filename = clean_filename.replace(" ", "_")

        return clean_filename 
    