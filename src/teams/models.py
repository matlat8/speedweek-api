

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, UUID
from datetime import datetime

from src.core.db import Base

class Team(Base):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    
    def __repr__(self):
        return f"<Team {self.name}>"
    
class UserTeam(Base):
    __tablename__ = "user_team"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("team.id"), nullable=False)
    is_team_admin = Column(Boolean, nullable=False, default=False) # if true, user can manage team
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    
    def __repr__(self):
        return f"<UserTeam {self.id}>"
    