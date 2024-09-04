from fastapi import APIRouter, Depends

from src.auth.users import User, current_active_user
from src.core.db import get_db_session

from src.leagues.crud import create_new_league, get_leagues
from src.leagues.schemas import NewLeague

from src.seasons.router import seasons as seasons_router

leagues = APIRouter(prefix="/leagues")

@leagues.get("")
async def rt_get_leagues(user: User = Depends(current_active_user), db = Depends(get_db_session)):
    leagues_data = await get_leagues(db=db, user_id=user.id)
    return {"data": leagues_data}

@leagues.post("")
async def create_league(league: NewLeague, db = Depends(get_db_session), user: User = Depends(current_active_user)):
    new_league = await create_new_league(db=db, league_name=league.name, owner_id=user.id)
    return {"league": new_league}

@leagues.get("/{league_id}")
async def get_league(league_id: int):
    return {"league": league_id}

@leagues.put("/{league_id}")
async def update_league(league_id: int):
    return {"league": league_id}

@leagues.delete("/{league_id}")
async def delete_league(league_id: int):
    return {"league": league_id}

@leagues.patch("/{league_id}")
async def patch_league(league_id: int):
    return {"league": league_id}

leagues.include_router(seasons_router)
