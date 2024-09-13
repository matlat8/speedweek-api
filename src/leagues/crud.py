import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import uuid

from src.core.utils import to_pydantic_list
from src.auth.models import User
from src.leagues.models import League, LeagueUser
from src.leagues.schemas import LeagueMembersResponse
from src.leagues.utils import generate_invite_token

async def get_leagues(db: AsyncSession, user_id: uuid.UUID):
    query = select(League)
    result = await db.execute(query)
    return result.scalars().all()

async def get_a_league(db: AsyncSession, league_id: int):
    query = select(League).where(League.id == league_id)
    result = await db.execute(query)
    return result.scalars().first()

async def get_league_members(db: AsyncSession, league_id: int):
    query = select(LeagueUser.id,
                   LeagueUser.is_owner,
                   LeagueUser.is_admin,
                   User.id.label('user_id'),
                   User.display_name).join(LeagueUser).where(LeagueUser.league_id == league_id)
    result = await db.execute(query)
    members = result.all()
    return to_pydantic_list(LeagueMembersResponse, members)
async def get_user_joined_leagues(db: AsyncSession, user_id: uuid.UUID) -> list[League]:
    """
    Find all leagues that a user has joined
    """
    query = select(League).join(LeagueUser).where(LeagueUser.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().all()

async def create_new_league(db: AsyncSession, owner_id: uuid.UUID, league_name: str):
    league = League(name=league_name, owner_id=owner_id, invite_token=generate_invite_token())
    db.add(league)
    await db.commit()
    db.refresh(league)
    return league

async def add_user_to_league(db: AsyncSession, league_id: int, user_id: uuid.UUID):
    leagueuser = LeagueUser(league_id=league_id, user_id=user_id)
    db.add(leagueuser)
    await db.flush()
    await db.refresh(leagueuser)
    return leagueuser