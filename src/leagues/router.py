from fastapi import APIRouter, Depends

from src.auth.users import User, current_active_user
from src.core.db import get_db_session

from src.leagues.crud import create_new_league, get_leagues, get_a_league, add_user_to_league, get_league_members
from src.leagues.schemas import NewLeague


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
async def get_league(league_id: int, user: User = Depends(current_active_user), db = Depends(get_db_session)):
    league = await get_a_league(db=db, league_id=league_id)
    #league_members = await get_league_members(db=db, league_id=league_id)
    return {"info": league}

@leagues.get("/{league_id}/members")
async def get_league_members_route(league_id: int, db = Depends(get_db_session)):
    league_members = await get_league_members(db=db, league_id=league_id)
    return {"data": league_members}

# @leagues.put("/{league_id}")
# async def update_league(league_id: int):
#     return {"league": league_id}
# 
# @leagues.delete("/{league_id}")
# async def delete_league(league_id: int):
#     return {"league": league_id}
# 
# @leagues.patch("/{league_id}")
# async def patch_league(league_id: int):
#     return {"league": league_id}

@leagues.post("/{league_id}/join")
async def join_league(league_id: int, user: User = Depends(current_active_user), db = Depends(get_db_session)):
    userleague = await add_user_to_league(db=db, league_id=league_id, user_id=user.id)
    await db.commit()
    return {"league": userleague}
