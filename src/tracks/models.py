from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, UUID, UniqueConstraint

from datetime import datetime

from src.core.db import Base

class Track(Base):
    __tablename__ = "track"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    config = Column(String, nullable=True)
    iracing_id = Column(Integer, nullable=True)
    iracing_image_url = Column(String, nullable=True)
    garage61_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    
    UniqueConstraint('name', 'config', name='_track_config_uc')
    
    def __repr__(self):
        return f"<Track {self.name}>"