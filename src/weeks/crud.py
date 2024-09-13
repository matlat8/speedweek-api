from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
import uuid

from weeks.models import Week

async def create_week(db: AsyncSession,
                          week_num: int,
                          season_id: int):
    week = Week(week_num=week_num, season_id=season_id)
    db.add(week)
    await db.flush()
    await db.refresh(week)
    return week

async def get_seasons_latest_week(db: AsyncSession,
                              season_id: int) -> Week:
    query = select(Week).where(Week.season_id == season_id).order_by(Week.week_num.desc()).limit(1)
    result = await db.execute(query)
    return result.scalars().first()