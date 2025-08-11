from ..VectorDBInterface import VectorDBInterface 
import logging 
from qdrant_client import models , QdrantClient
from ..VectorDBEnums import DistanceMethodEnum 
from typing import List 

class QdrantDBProvider(VectorDBInterface):
    def __init__(self,
                 db_path : str,
                 distance_method : DistanceMethodEnum = str):

        self.client = None 
        self.db_path = db_path 
        self.distance_method = None  

        if distance_method == DistanceMethodEnum.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnum.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger(__name__) 

    def connect(self): 
        self.client = QdrantClient(path = self.db_path)   

    def disconnect(self):
        self.client = None 

    def is_collection_exist(self, collection_name)->bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collection(self)->List:
        return self.client.get_collections() 
    
    def get_collection_info(self, collection_name)->dict:
        return self.client.get_collection(collection_name = collection_name)
    
    def delete_collection(self, collection_name):
        if self.is_collection_exist(collection_name):
            return  self.client.delete_collection(collection_name = collection_name)
        
    def create_collection(self, collection_name, embedding_size, do_reset = False):
        if do_reset: 
            self.delete_collection(collection_name = collection_name)

        if not self.is_collection_exist(collection_name):

            _ = self.client.create_collection(collection_name = collection_name,
                                                vectors_config=models.VectorParams
                                                (size=embedding_size, distance=self.distance_method)
                                                )
        
            return True

        return False


    def insert_one(self,
                collection_name : str,
                text : str, vector: list,
                metadata : dict = None,
                record_id : str = None):
        try : 
            if not self.is_collection_exist(collection_name):
                self.logger.warning(f"Collection {collection_name} does not exist") 
                return False
            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        id=record_id,
                        vector=vector,
                        payload={
                            "text": text,
                            "metadata": metadata
                        }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error inserting record: {e}")
            return False

        return True

    def insert_many(self,
                collection_name : str,
                texts : List,
                vectors : list,
                metadata : list = None,
                record_ids : list = None,
                batch_size : int = 50):
        
        if metadata is None:
            metadata = [None] * len(texts) 

        if record_ids is None:
            record_ids = list(range(0, len(texts)))

        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_record_ids = record_ids[i:batch_end]

            batch_record = [
                models.Record(
                    id=batch_record_ids[x],
                    vector=batch_vectors[x],
                    payload= {
                        "text": batch_texts[x],
                        "metadata": batch_metadata[x]
                    }
                ) for x in range(len(batch_texts))
                    
            ] 
            try  :
                _ = self.client.upload_records(
                    collection_name=collection_name,
                    records=batch_record,
                ) 
            except Exception as e:
                self.logger.error(f"Error inserting records: {e}")
                return False
                
        return True 

    def search_by_vector(self, collection_name: str,
                        vector: list, limit : int = 5):
        return self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit,
        ) 
    
    