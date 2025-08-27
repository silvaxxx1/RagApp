from .RagApp_base import SQLAlchemyBase 
from sqlalchemy import Column, Integer,DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Index
from datetime import datetime   
import uuid 

class Asset(SQLAlchemyBase):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, autoincrement=True) 
    asset_uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, nullable=False)

    asset_type = Column(String, nullable=False)
    asset_name = Column(String, nullable=False)
    asset_size = Column(Integer, nullable=False) 
    asset_config = Column(JSONB, nullable=True)

    asset_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)

    project = relationship("Project", back_populates="assets") 

    __table_args__ = (
        Index('ix_asset_project_id', asset_project_id),
        Index('ix_asset_type', asset_type),
                    )