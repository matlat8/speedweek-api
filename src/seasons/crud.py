from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
import uuid

from src.seasons.models import Season

async def create_season(db: AsyncSession,
                        name: str,
                        start_date: str,
                        end_date: str,
                        league_id: int,
                        season_num: int):
    season = Season(name=name, start_date=start_date, end_date=end_date, league_id=league_id, season_num=season_num)
    db.add(season)
    await db.flush()
    await db.refresh(season)
    return season

async def get_league_seasons(db: AsyncSession,
                             league_id: int):
    query = select(Season).where(Season.league_id == league_id)
    result = await db.execute(query)
    return result.scalars().all()

async def get_active_seasons(db: AsyncSession, league_ids: List[int]):
    query = select(Season) \
        .where(Season.league_id.in_(league_ids)) \
        .where(Season.start_date <= datetime.now()) \
        .where(Season.end_date >= datetime.now())
    result = await db.execute(query)
    return result.scalars().all()