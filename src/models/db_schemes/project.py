from pydantic import BaseModel, Field, field_validator , ConfigDict
from typing import Optional 
from bson import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    model_config = ConfigDict(
        arbitrary_types_allowed=True  # Needed for ObjectId
    )

    @field_validator('project_id')
    def validate_project_id(cls, project_id):
        if not project_id.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return project_id 
    
    @classmethod
    def get_indexes(cls):
        return [
                {
                    "key": [
                        ("project_id", 1) # 1 for ascending
                    ],
                    "name": "project_id_index_1",
                    "unique": True
                }
        ]
