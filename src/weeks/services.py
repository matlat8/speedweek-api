from sqlalchemy.ext.asyncio import AsyncSession

from weeks.models import Week
from weeks import crud

async def create_new_week(db: AsyncSession,
                          league_id: int,
                          season_id: int,) -> Week:
    latest_week = await crud.get_seasons_latest_week(db=db, season_id=season_id)
    if not latest_week:
        week_num = 1
    else:
        week_num = latest_week.week_num + 1
        
    week = await crud.create_week(db=db, week_num=week_num, season_id=season_id)
    
    await db.commit()
    
    return week