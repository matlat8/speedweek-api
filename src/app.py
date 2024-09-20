from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import contextlib

from src.config import  settings
from src.log_config import logger
from src.auth.router import auth
from src.leagues.router import leagues
from src.teams.router import teams
from src.seasons.router import seasons
from src.weeks.router import weeks
from src.cars.router import cars
from src.tracks.router import tracks

from version import __version__

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "https://speedweektt.com"],  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth)
app.include_router(leagues)
app.include_router(teams)
app.include_router(seasons)
app.include_router(weeks)
app.include_router(cars)
app.include_router(tracks)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f'{settings.app_name} v{__version__} starting up')

    yield
    logger.info(f'{settings.app_name} v{__version__} shutting down')

@app.get("/")
def read_root():
    return {"Hello": "World"}

