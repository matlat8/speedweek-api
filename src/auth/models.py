from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Column, String

from src.core.db import Base 

class User(SQLAlchemyBaseUserTableUUID, Base):
    display_name = Column(String, nullable=True)
    