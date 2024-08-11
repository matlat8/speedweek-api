from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from src.core.db import Base 

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass