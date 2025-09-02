from .RagApp_base import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Project(SQLAlchemyBase):
    __tablename__ = "projects"
    
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    project_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # For initial insertion
        onupdate=func.now(),        # For updates
        nullable=False              # Ensures no NULL values
    )

    chunks = relationship("DataChunk", back_populates="project")
    assets = relationship("Asset", back_populates="project")
