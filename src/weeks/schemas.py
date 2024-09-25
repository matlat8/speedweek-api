from pydantic import BaseModel
import src.tracks.models
import src.weeks.models
from typing import Optional
from datetime import datetime

from src.cars.schemas import CarModel
from src.tracks.schemas import TrackModel

class NewWeek(BaseModel):
    track_id: int
    car_id: int
    start_date: datetime
    end_date: datetime


    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
class WeekModel(BaseModel):
    id: int
    week_num: int
    season_id: int
    track_id: int
    car_id: int
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
    
    
class WeekWithDetails(BaseModel):
    week: WeekModel
    track: TrackModel
    car: CarModel
    
    class Config:
        from_attributes = True

