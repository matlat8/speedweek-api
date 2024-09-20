from fastapi import APIRouter, Depends
import httpx
from src.auth.users import User, current_active_user
from src.core.db import get_db_session
from src.core.garage61_client import get_garage_client
from src.weeks.services import create_new_week, season_weeks, get_week_laps
from src.weeks.schemas import NewWeek

weeks = APIRouter(prefix="/leagues/{league_id}/seasons/{season_id}/weeks")

@weeks.get("")
async def rt_get_weeks(league_id: int, season_id: int, 
                       user: User = Depends(current_active_user), 
                       db = Depends(get_db_session)):
    weeks_data = await season_weeks(db=db, season_id=season_id)
    
    return {"data": weeks_data}

@weeks.post("")
async def rt_create_week(league_id: int, season_id: int, new_week: NewWeek,
                         user: User = Depends(current_active_user), 
                         db = Depends(get_db_session)):
    
    new_week = await create_new_week(db=db, league_id=league_id, season_id=season_id, user_id=user.id, new_week=new_week)
    
    return {"data": new_week}

@weeks.get('/{week_id}/laps')
async def get_garage61_laps(week_id: int,
                            user: User = Depends(current_active_user),
                            db = Depends(get_db_session),
                            garage_client: httpx.AsyncClient = Depends(get_garage_client)):
    week = await get_week_laps(db=db, garage_client=garage_client, week_id=week_id)
    return {"data": week}