from pydantic import BaseModel

class NewTrack(BaseModel):
    name: str
    config: str = None
    iracing_id: int = None
    iracing_image_url: str = None
    garage61_id: int = None
    