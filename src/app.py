from fastapi import FastAPI
import contextlib

from src.config import  settings
from src.log_config import logger
from src.auth.router import auth
from src.leagues.router import leagues
from version import __version__

app = FastAPI()

app.include_router(auth)
app.include_router(leagues)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f'{settings.app_name} v{__version__} starting up')

    yield
    logger.info(f'{settings.app_name} v{__version__} shutting down')

@app.get("/")
def read_root():
    return {"Hello": "World"}

