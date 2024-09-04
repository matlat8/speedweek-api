from fastapi import APIRouter, Depends

from src.auth.users import User, current_active_user
from src.core.db import get_db_session

seasons = APIRouter(prefix="/league/{league_id}/seasons")

@seasons.get("")
async def rt_get_seasons(league_id: int, 
                         user: User = Depends(current_active_user), 
                         db = Depends(get_db_session)):
    return {"data": []}

@seasons.post("")
async def create_season(user: User = Depends(current_active_user), 
                        db = Depends(get_db_session)):
    return {"data": []}

@seasons.get("/{season_id}")
async def get_season(season_id: int):
    return {"data": []}
