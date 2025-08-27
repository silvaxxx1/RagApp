from .RagApp_base import SQLAlchemyBase 
from sqlalchemy import Column, Integer,DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Index
from datetime import datetime   
import uuid  

from pydantic import BaseModel


class Chunk(SQLAlchemyBase):
    __tablename__ = "chunks"

    chunk_id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False)
    chunk_text = Column(String, nullable=False)
    chuck_metadata = Column(JSONB, nullable=True)
    chuck_order = Column(Integer, nullable=False)

    
    chunk_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    chunk_asset_id = Column(Integer, ForeignKey("assets.asset_id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
    
    project = relationship("Project", back_populates="chunks")
    assets = relationship("Asset", back_populates="chunks") 

    __table_args__ = (
        Index('ix_chunk_project_id', chunk_project_id),
        Index('ix_chunk_asset_id', chunk_asset_id),
    ) 


class RetrievalDocument(BaseModel):
    text: str
    score: float
