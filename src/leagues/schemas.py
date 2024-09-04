from pydantic import BaseModel

class NewLeague(BaseModel):
    """
    Parameters needed to create a new league
    """
    name: str
    