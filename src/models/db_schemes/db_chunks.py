from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

class DataChunk(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chuck_metadata: dict 
    chuck_project_id: ObjectId 

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True  # Needed for ObjectId
    )