from helpers.config import get_settings
import os

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
