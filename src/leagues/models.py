import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Boolean, ARRAY

from src.core.db import Base

AssetsBase = declarative_base(metadata=Base.metadata)

class League(Base):
    __tablename__ = "leagues"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brandpartner_owner_id = Column(Integer, ForeignKey("brandpartner.id"), nullable=False) # not used to assign ownership, but to track which brandpartner the asset belongs to
    created_at = Column(TIMESTAMP, default=arrow.utcnow().datetime.replace(tzinfo=None))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    updated_at = Column(TIMESTAMP, default=arrow.utcnow().datetime.replace(tzinfo=None))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    