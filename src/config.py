from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "SpeedWeek API"
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str


    class Config:
        env_file = ".env"
    
@lru_cache()   
def get_settings():
    return Settings() 

settings = get_settings()