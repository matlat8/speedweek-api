from pydantic import BaseModel
from uuid import UUID

class NewLeague(BaseModel):
    """
    Parameters needed to create a new league
    """
    name: str
    
    
class LeagueMembersResponse(BaseModel):
    id: int
    is_owner: bool
    is_admin: bool
    user_id: UUID
    display_name: str
    
    class Config:
        from_attributes = True
    
    