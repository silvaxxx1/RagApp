from .BaseDataModel import BaseDataModel 
from .db_schemes import DataChunk 
from helpers.config import get_settings
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        self.app_settings = get_settings()
        self.db_client = db_client 
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNCK_NAME.value] 

    
    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.dict(by_alias=True,exclude_unset=True))
        chunk._id = result.inserted_id

        return chunk 
    
    async def get_chunck(self, chunk_id: str):
        result = await self.collection.find_one({
                            "_id": ObjectId(chunk_id)
                                                }) 
        
        if result is None:
            return None

        return DataChunk(**result) 



    async def get_many_chunks(self,
                            chuncks : list,
                            batch_size: int = 100
                            ):
        
        for i in range(0, len(chuncks), batch_size):
            batch = chuncks[i:i + batch_size]
            operations = [
                InsertOne(chunk.dict(by_alias=True,exclude_unset=True)) 
                for chunk in batch
                        ]
            await self.collection.bulk_write(operations)

        return len(chuncks) 
    
    async def delete_chunk_by_id  (self, project_id: ObjectId):
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })