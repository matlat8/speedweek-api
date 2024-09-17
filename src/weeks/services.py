from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from datetime import datetime, timezone

from uuid import UUID
from src.leagues.crud import get_league_members
from src.weeks.models import Week
from src.weeks.schemas import NewWeek
from src.weeks import crud

async def create_new_week(db: AsyncSession,
                          league_id: int,
                          season_id: int,
                          new_week: NewWeek,
                          user_id: UUID) -> Week:
    league_members = await get_league_members(db=db, league_id=league_id)
    if not any(member.user_id == user_id for member in league_members):
        raise HTTPException(status_code=403, detail="User is not an administrator of this league.")
    
    new_week.start_date = make_offset_aware(new_week.start_date)
    new_week.end_date = make_offset_aware(new_week.end_date)
    
    latest_week = await crud.get_seasons_latest_week(db=db, season_id=season_id)
    if not latest_week:
        week_num = 1
    else:
        week_num = latest_week.week_num + 1
        
    week = await crud.create_week(db=db, week_num=week_num, season_id=season_id, new_week=new_week)
    
    await db.commit()
    
    return week

def make_offset_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


async def season_weeks(db: AsyncSession, season_id: int):
    data = await crud.get_season_weeks(db=db, season_id=season_id)
    weeks = []
    for week, track, car in data:
        week_data = week.__dict__
        week_data['track'] = track.__dict__
        week_data['car'] = car.__dict__
        weeks.append(week_data)
    
    return weeks