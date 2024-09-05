from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
import uuid

from src.teams.schemas import TeamsResponse
from src.teams.models import Team, UserTeam
from src.auth.models import User


async def get_teams(db: AsyncSession, user_id: uuid.UUID):
    team_members_subquery = (
        select(UserTeam.team_id, func.count(UserTeam.user_id).label("team_members"))
        .group_by(UserTeam.team_id)
        .subquery()
    )

    query = (
        select(
            Team.name,
            Team.owner_id,
            User.display_name,
            team_members_subquery.c.team_members
        )
        .join(UserTeam, UserTeam.team_id == Team.id)
        .join(User, User.id == Team.owner_id)
        .outerjoin(team_members_subquery, team_members_subquery.c.team_id == Team.id)
        .where(UserTeam.user_id == user_id)
    )
    result = await db.execute(query)
    teams = result.all()
    return [TeamsResponse.from_orm(team) for team in teams]

async def create_team(db: AsyncSession, team_name: str, owner_id: uuid.UUID):
    team = Team(name=team_name, owner_id=owner_id)
    db.add(team)
    await db.flush()
    await db.refresh(team)
    return team

async def add_user_to_team(db: AsyncSession, team_id: int, user_id: uuid.UUID, is_team_admin: bool):
    user_team = UserTeam(team_id=team_id, user_id=user_id, is_team_admin=is_team_admin)
    db.add(user_team)
    await db.flush()
    await db.refresh(user_team)
    return user_team