import datetime
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException

import src.auth.models
from src.core.db import get_db_session
from src.auth.users import User, current_active_user
from src.auth.models import Garage61User
from src.config import settings

# garage_client = httpx.AsyncClient(base_url='https://garage61.net',
#                                   headers={'Authorization': 'Bearer ' + garage61_access_token})

async def get_garage_client(db: AsyncSession = Depends(get_db_session),
                            user: User = Depends(current_active_user)):
    tokens = await get_garage_tokens(db, user.id)
    if not tokens:
        raise HTTPException(status_code=401, detail="Garage61 account not linked")
    if tokens.garage61_access_token_expires < datetime.datetime.utcnow():
        tokens = await refresh_garage_access_token(tokens)
        await db.flush()
        
    headers = {
        'Authorization': f'Bearer {tokens.garage61_access_token}' 
    }
    garage_client = httpx.AsyncClient(
        base_url='https://garage61.net/',
        headers=headers,
    )
    print(headers)
    
    return garage_client

async def get_garage_tokens(db: AsyncSession,
                            user_id: str):
    query = select(Garage61User).where(Garage61User.linked_account_id == user_id)
    result = await db.execute(query)
    return result.scalars().first()

async def refresh_garage_access_token(tokens: Garage61User) -> Garage61User:
    print('we gotta refresh this token....')
    url = 'https://garage61.net/api/oauth/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': tokens.garage61_refresh_token,
        'client_id': settings.garage61_client_id,
        'client_secret': settings.garage61_client_secret,
        'scope': 'driving_data',
        'redirect_uri': 'https://api.speedweektt.com/auth/garage61/callback'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    with httpx.Client() as client:
        response = client.post(url, data=data, headers=headers)
        if response.status_code != 200:
            print(response.content)
            raise HTTPException(status_code=response.status_code, detail='Failed to refresh token')
        tokens.garage61_access_token = response.json()['access_token']
        tokens.garage61_refresh_token = response.json()['refresh_token']
        tokens.garage61_access_token_expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=response.json()['expires_in'])
        print(response.content)
        return tokens