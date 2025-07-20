from typing import Optional
from pydantic import BaseModel , Field , validator
from bson import ObjectId

class DataChunk(BaseModel):
    _id: Optional[ObjectId]
    chunk_text : str = Field(..., min_length=1)
    chuck_metadata : dict 
    chuck_project_id : ObjectId 

    class Config:
        allow_population_by_field_name = True