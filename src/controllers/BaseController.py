from helpers.config import get_settings
import os
import random 
import string

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()

        # ✅ Go to src/ (parent of controllers/)
        self.base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

        # ✅ assets/files now resolves to src/assets/files/
        self.files_dir = os.path.join(self.base_dir, "assets/files")

        os.makedirs(self.files_dir, exist_ok=True)  # optional: auto-create

        self.database_dir = os.path.join(
                                    self.base_dir,
                                    "assets/database"
                                    )
        
    def generate_random_string(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    def get_database_path(self, db_name: str):
        database_path = os.path.join(self.database_dir, db_name)

        if not os.path.exists(database_path):
            os.makedirs(database_path)

        return database_path
        