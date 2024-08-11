from fastapi import APIRouter

leagues = APIRouter(prefix="/leagues")

@leagues.get("")
async def get_leagues():
    return {"leagues": "list of leagues"}

@leagues.post("")
async def create_league():
    return {"league": "created league"}

@leagues.get("/{league_id}")
async def get_league(league_id: int):
    return {"league": league_id}

@leagues.put("/{league_id}")
async def update_league(league_id: int):
    return {"league": league_id}

@leagues.delete("/{league_id}")
async def delete_league(league_id: int):
    return {"league": league_id}

@leagues.patch("/{league_id}")
async def patch_league(league_id: int):
    return {"league": league_id}

