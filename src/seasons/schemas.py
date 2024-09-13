from pydantic import BaseModel
import datetime

class NewSeason(BaseModel):
    """
    Parameters needed to create a new season
    """
    name: str
    start_date: datetime.date
    end_date: datetime.date