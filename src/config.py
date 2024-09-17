from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "SpeedWeek API"
    db_user: str
    db_pass: str
    db_host: str
    db_port: int
    db_name: str
    jwt_secret: str


    class Config:
        env_file = "./.env"
        extra = 'ignore'
    
@lru_cache()   
def get_settings():
    return Settings() 

settings = get_settings()