from fastapi import APIRouter, Depends

from src.auth.users import User, current_active_user
from src.core.db import get_db_session

from src.leagues.crud import get_leagues, get_user_joined_leagues

from src.seasons.schemas import NewSeason
from src.seasons.crud import create_season, get_league_seasons, get_active_seasons, get_season_info

seasons = APIRouter(prefix="/leagues/{league_id}/seasons")

# /league/{league_id}/seasons
@seasons.get("")
async def rt_get_seasons(league_id: int, 
                         user: User = Depends(current_active_user), 
                         db = Depends(get_db_session)):
    
    leagues = await get_user_joined_leagues(db=db, user_id=user.id)
    league_ids = [league.id for league in leagues]
    print(league_ids)
    #active_seasons = await get_active_seasons(db=db, league_ids=[league_id])
    season = await get_league_seasons(db=db, league_id=league_id)
    
    return {"data": season}

# /league/{league_id}/seasons
@seasons.post("")
async def rt_create_season(season: NewSeason,
                        league_id: int,
                        user: User = Depends(current_active_user), 
                        db = Depends(get_db_session)):
    seasonn = await create_season(db=db, name=season.name, start_date=season.start_date, end_date=season.end_date, league_id=league_id, season_num=1)
    await db.commit()
    
    return {"data": seasonn}

# /league/{league_id}/seasons/{season_id}
@seasons.get("/{season_id}")
async def get_season(season_id: int, league_id: int, db = Depends(get_db_session)):
    #season = await get_league_seasons(db=db, league_id=league_id)
    season = await get_season_info(db=db, season_id=season_id)
    
    return {"info": season}
