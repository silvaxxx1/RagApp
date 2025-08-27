from pydantic import BaseModel, Field, field_validator , ConfigDict
from typing import Optional 
from bson import ObjectId
from datetime import datetime 

class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id: ObjectId 
    asset_type: str = Field(..., min_length=1) 
    asset_name : str = Field(..., min_length=1) 
    aseet_size : int = Field(ge=0, default=None)
    asset_pushed_at : datetime = Field(default=datetime.utcnow) 
    asset_config : dict = Field(default=None)
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True  # Needed for ObjectId
    )

    
    @classmethod
    def get_indexes(cls):
        return [
                {
                    "key": [
                        ("asset_project_id", 1) # 1 for ascending
                    ],
                    "name": "project_id_index_1",
                    "unique": False
                },
                {
                    "key": [
                        ("asset_type", 1),
                        ("asset_name" , 1) # 1 for ascending
                    ],
                    "name": "asset_project_id_index_1",
                    "unique": True
                }
        ]

    