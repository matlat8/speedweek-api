from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.tracks.models import Track
from src.tracks.schemas import NewTrack

async def create_new_track(db: AsyncSession, track: NewTrack):
    new_track = Track(**track.dict())
    db.add(new_track)
    return new_track


async def get_all_tracks(db: AsyncSession):
    query = select(Track)
    tracks = await db.execute(query)
    tracks_data = tracks.scalars().all()
    
    return tracks_data


