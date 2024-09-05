from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import uuid

from src.seasons.models import Season

async def create_season(db: AsyncSession,
                        name: str,
                        start_date: str,
                        end_date: str,
                        league_id: int):
    season = 
    
    pass