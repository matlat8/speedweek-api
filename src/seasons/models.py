import asyncio
from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, select, func, event
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import relationship
from datetime import datetime

from src.core.db import Base

class Season(Base):
    __tablename__ = "season"
    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("league.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    season_num = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    
    league = relationship("League", back_populates="seasons")