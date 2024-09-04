import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import uuid

from src.leagues.models import League
from src.leagues.utils import generate_invite_token

async def get_leagues(db: AsyncSession, user_id: uuid.UUID):
    query = select(League)
    result = await db.execute(query)
    return result.scalars().all()

async def create_new_league(db: AsyncSession, owner_id: uuid.UUID, league_name: str):
    league = League(name=league_name, owner_id=owner_id, invite_token=generate_invite_token())
    db.add(league)
    await db.commit()
    db.refresh(league)
    return league