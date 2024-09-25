from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewTrack(BaseModel):
    name: str
    config: str = None
    iracing_id: int = None
    iracing_image_url: str = None
    garage61_id: int = None
    
    
class TrackModel(BaseModel):
    id: int
    name: str
    config: Optional[str]
    iracing_id: Optional[int]
    iracing_image_url: Optional[str]
    garage61_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True