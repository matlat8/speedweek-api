from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.users import fastapi_users, jwt_auth_backend, cookie_auth_backend, current_active_user, User
from src.core.db import get_db_session
from src.auth.schema import UserRead, UserUpdate
from src.config import settings
from src.auth import services

auth = APIRouter()

auth.include_router(fastapi_users.get_auth_router(backend=jwt_auth_backend), prefix="/auth/jwt", tags=["auth"])
auth.include_router(fastapi_users.get_auth_router(backend=cookie_auth_backend), prefix="/auth/cookie", tags=["auth"])
auth.include_router(fastapi_users.get_register_router(UserRead, UserUpdate), prefix="/auth", tags=["auth"])
auth.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

@auth.get('/auth/garage61')
async def garage61_auth():
    url = 'https://garage61.net/app/account/oauth'
    params = {
        'client_id': settings.garage61_client_id,
        'redirect_uri': 'https://api.speedweektt.com/auth/garage61/callback',
        'scope': 'driving_data',
        'response_type': 'code'
    }
    return {"url": url + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])}

@auth.get('/auth/garage61/callback')
async def garage61_callback(code: str, user: User = Depends(current_active_user), db: AsyncSession = Depends(get_db_session)):
    codes = await services.handle_callback(code, db, user.id)
    return RedirectResponse(url='https://speedweektt.com')
