from fastapi import APIRouter

from src.auth.users import fastapi_users, jwt_auth_backend, cookie_auth_backend
from src.auth.schema import UserRead, UserUpdate

auth = APIRouter()

auth.include_router(fastapi_users.get_auth_router(backend=jwt_auth_backend), prefix="/auth/jwt", tags=["auth"])
auth.include_router(fastapi_users.get_auth_router(backend=cookie_auth_backend), prefix="/auth/cookie", tags=["auth"])
auth.include_router(fastapi_users.get_register_router(UserRead, UserUpdate), prefix="/auth", tags=["auth"])
auth.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)