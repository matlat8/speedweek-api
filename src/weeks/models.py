from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, UUID, UniqueConstraint
from datetime import datetime

from src.core.db import Base

class Week(Base):
    __tablename__ = "week"
    id = Column(Integer, primary_key=True, index=True)
    week_num = Column(Integer, nullable=False)
    season_id = Column(Integer, ForeignKey("season.id"), nullable=False)
    car_id = Column(Integer, ForeignKey("car.id", ondelete='CASCADE'), nullable=False)
    track_id = Column(Integer, ForeignKey("track.id", ondelete='CASCADE'), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    
    __table_args__ = (UniqueConstraint('week_num', 'season_id', name='_week_season_uc'),)
    
    def __repr__(self):
        return f"<Week {self.id}>"
    
class Result(Base):
    __tablename__ = "result"
    id = Column(Integer, primary_key=True, index=True)
    week_id = Column(Integer, ForeignKey("week.id"), nullable=False)
    driver_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    laptime = Column(Float, nullable=False) # in seconds
    points = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())