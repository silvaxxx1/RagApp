from .RagApp_base import SQLAlchemyBase 
from sqlalchemy import Column, Integer,DateTime, func
from sqlalchemy.dialects.postgresql import UUID 
from datetime import datetime   
import uuid

class Project(SQLAlchemyBase):
    __tablename__ = "projects" 

    project_id = Column(Integer, primary_key=True, autoincrement=True) 
    project_uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False) 




