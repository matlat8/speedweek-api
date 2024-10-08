from pydantic import BaseModel
import uuid

class NewTeam(BaseModel):
    name: str
    
class TeamsResponse(BaseModel):
    name: str
    owner_id: uuid.UUID
    display_name: str
    team_members: int
    
    class Config:
        from_attributes = True