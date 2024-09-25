import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from datetime import datetime, timezone

from uuid import UUID
from src.leagues.crud import get_league_members
from src.weeks.models import Week
from src.weeks.schemas import NewWeek
from src.weeks import crud
from src.weeks import g61

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

async def get_week(db: AsyncSession, week_id: int):
    week = await crud.get_week(db=db, week_id=week_id)
    return week

async def get_week_laps(db: AsyncSession, garage_client: httpx.AsyncClient, week_id: int):
    week = await crud.get_week(db=db, week_id=week_id)
    end_date_aware = make_offset_aware(week.week.end_date)
    current_time_aware = datetime.now(timezone.utc)
    print(week.track.iracing_id)
    if end_date_aware > current_time_aware:
        data = await g61.get_laps(week.car.garage61_car_id, week.track.garage61_id, week.week.start_date, garage_client)
    else:
        # database result laps
        data = await g61.get_laps(week.car.garage61_car_id, week.track.garage61_id, week.start_date, garage_client) 
    
    return data

