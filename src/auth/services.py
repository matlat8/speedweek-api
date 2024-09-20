from datetime import timedelta, datetime
import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from src.auth.models import Garage61User

import src.auth.models
from src.config import settings
async def handle_callback(code: str, db: AsyncSession, user_id):
    async with httpx.AsyncClient() as client:
        response = await client.post('https://garage61.net/api/oauth/token', data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'https://api.speedweektt.com/auth/garage61/callback',
            'client_id': settings.garage61_client_id,
            'client_secret': settings.garage61_client_secret,
        }, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail='oopsie')
        
        codes = response.json()
        expiration_datetime = datetime.utcnow() + timedelta(seconds=codes['expires_in'])
        
        # Check if the user already exists
        query = select(Garage61User).where(Garage61User.linked_account_id == user_id)
        result = await db.execute(query)
        existing_user = result.scalars().first()
        
        if existing_user:
            # Update the existing user
            existing_user.garage61_access_token = codes['access_token']
            existing_user.garage61_refresh_token = codes['refresh_token']
            existing_user.garage61_access_token_expires = expiration_datetime
        else:
            # Create a new user
            linked_user = Garage61User(
                linked_account_id=user_id,
                garage61_access_token=codes['access_token'],
                garage61_refresh_token=codes['refresh_token'],
                garage61_access_token_expires=expiration_datetime,
            )
            db.add(linked_user)
        
        await db.commit()
        
        return response.json()