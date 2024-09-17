from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, UUID, Enum as SqlEnum
from datetime import datetime
from enum import Enum

from src.core.db import Base

class CarCategory(Enum):
    SPORTS_CAR = "sports_car"
    FORMULA_CAR = "formula_car"
    OVAL = "oval"
    DIRT_OVAL = "dirt_oval"
    

class Car(Base):
    __tablename__ = "car"
    id = Column(Integer, primary_key=True, index=True)
    car_name = Column(String, nullable=False, unique=True)
    car_category = Column(SqlEnum(CarCategory), nullable=True)
    iracing_car_id = Column(Integer, nullable=True)
    iracing_car_picture = Column(String, nullable=True)
    garage61_car_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)