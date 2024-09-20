from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy import Column, String, Integer, DateTime, UUID, ForeignKey
from datetime import datetime

from src.core.db import Base 

class User(SQLAlchemyBaseUserTableUUID, Base):
    display_name = Column(String, nullable=True)
    
    
class Garage61User(Base):
    __tablename__ = "garage61_user"
    id = Column(Integer, primary_key=True, index=True)
    linked_account_id = Column(UUID, ForeignKey("user.id"), nullable=False, unique=True)
    garage61_access_token = Column(String, nullable=False)
    garage61_refresh_token = Column(String, nullable=False)
    garage61_access_token_expires = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    
    def __repr__(self):
        return f"<Garage61User {self.id}>"
    
