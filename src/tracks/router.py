from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db_session
from src.auth.users import current_active_user, User
from src.tracks.schemas import NewTrack
from src.tracks.crud import create_new_track, get_all_tracks

tracks = APIRouter(prefix="/tracks")

@tracks.get("")
async def rt_get_tracks(db: AsyncSession = Depends(get_db_session), user = Depends(current_active_user)):
    track_data = await get_all_tracks(db)
    return {"data": track_data}

@tracks.post("")
async def rt_create_new_track(new_track: NewTrack, db: AsyncSession = Depends(get_db_session), user = Depends(current_active_user)):
    new_track = await create_new_track(db=db, track=new_track)
    await db.commit()
    return {"data": new_track}