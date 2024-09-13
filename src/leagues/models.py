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
    seasons = relationship("Season", back_populates="league", cascade="all, delete-orphan")

class LeagueUser(Base):
    __tablename__ = "league_user"
    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("league.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    is_owner = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    is_member = Column(Boolean, nullable=False, default=True)
    is_pending = Column(Boolean, nullable=False, default=False)
    is_banned = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, default=datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.now())
    UniqueConstraint('league_id', 'user_id', name='unique_league_user')
    