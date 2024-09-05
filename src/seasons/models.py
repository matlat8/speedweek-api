from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime

from src.core.db import Base

class Season(Base):
    __tablename__ = "season"
    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("league.id"), nullable=False)
    name = Column(String, nullable=False)
    season_num = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False)
    