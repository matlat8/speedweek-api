from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewWeek(BaseModel):
    track_id: int
    car_id: int
    start_date: datetime
    end_date: datetime


    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
