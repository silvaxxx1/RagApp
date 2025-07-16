from helpers.config import Settings , get_settings
class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
    

