import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Boolean, ARRAY
from datetime import datetime

from src.core.db import Base

class League(Base):
    __tablename__ = "league"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    discord_guild_id = Column(String, nullable=True)
    visibility = Column(Boolean, nullable=False, default=True) # Public or Private
    invite_token = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.now())

    