from .providers import QdrantDBProvider
from .VectorDBInterface import VectorDBInterface 
from .VectorDBEnums import VectorDBEnums 
from typing import List 
from . import VectorDBProvidersEnum
from controllers.BaseController import BaseController 




class VectorDBProvidersFactory:
    def __init__(self, config):
        self.config = config
        self.base_controller = BaseController()
        
    def create(self, provider: str):
        if provider == VectorDBProvidersEnum.QDRANT.value:
            db_path = self.base_controller.get_database_path(
                database_name = self.config.VECTOR_DB_NAME
            )
            return QdrantDBProvider(
                db_path = db_path,
                distance_method = self.config.VECTOR_DB_METHOD
            )

        return None 