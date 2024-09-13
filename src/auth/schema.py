import uuid
from typing import Optional
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    display_name: Optional[str] = None
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass