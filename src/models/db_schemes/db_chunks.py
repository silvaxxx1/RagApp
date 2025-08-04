from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

class DataChunk(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chuck_metadata: dict 
    chunk_order: int = Field(..., ge=0)
    chuck_project_id: ObjectId 
    chunk_asset_id: ObjectId 

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True  # Needed for ObjectId
    ) 

    @classmethod
    def get_indexes(cls):
        return [
                {
                    "key": [
                        ("chunk_project_id", 1) # 1 for ascending
                    ],
                    "name": "chunk_project_id_index_1",
                    "unique": False
                }
        ]