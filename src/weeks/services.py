from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from uuid import UUID
from leagues.crud import get_league_members
from weeks.models import Week
from weeks import crud

async def create_new_week(db: AsyncSession,
                          league_id: int,
                          season_id: int,
                          user_id: UUID) -> Week:
    league_members = await get_league_members(db=db, league_id=league_id)
    if not any(member.user_id == user_id for member in league_members):
        raise HTTPException(status_code=403, detail="User is not an administrator of this league.")
    
    latest_week = await crud.get_seasons_latest_week(db=db, season_id=season_id)
    if not latest_week:
        week_num = 1
    else:
        week_num = latest_week.week_num + 1
        
    week = await crud.create_week(db=db, week_num=week_num, season_id=season_id)
    
    await db.commit()
    
    return week