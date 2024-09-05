from fastapi import APIRouter, Depends

from src.auth.users import User, current_active_user
from src.core.db import get_db_session

from src.teams.crud import create_team, add_user_to_team, get_teams
from src.teams.schemas import NewTeam

teams = APIRouter(prefix="/teams")

@teams.get("")
async def rt_get_teams(db = Depends(get_db_session), user: User = Depends(current_active_user)):
    teamms = await get_teams(db, user.id)
    return {"data": teamms}

@teams.post("")
async def rt_create_team(team: NewTeam,
                      db = Depends(get_db_session), 
                      user: User = Depends(current_active_user)):
    teamm = await create_team(db=db, team_name=team.name, owner_id=user.id)
    print(teamm)
    userteam = await add_user_to_team(db=db, team_id=teamm.id, user_id=user.id, is_team_admin=True)
    await db.commit()
    return {"data": teamm}
    

@teams.get("/{team_id}")
async def get_team(team_id: int):
    return {"data": []}