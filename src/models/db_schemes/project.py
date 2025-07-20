from pydantic import BaseModel , Field , validator
from typing import Optional 
from bson import ObjectId


class Project(BaseModel):
    _id: Optional[ObjectId]
    project_id: str = Field(..., min_length=1)


    @validator('project_id')
    def validate_project_id(cls, project_id):
        if not project_id.isalnum():
            raise ValueError("project_id must be alphanumeric")
        return project_id
