from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from datetime import datetime
import uuid

from src.weeks import schemas
from src.weeks.models import Week
from src.tracks.models import Track
from src.cars.models import Car
from src.auth.models import Garage61User

from src.tracks.schemas import TrackModel
from src.cars.schemas import CarModel
from src.weeks.schemas import WeekModel


async def create_week(db: AsyncSession,
                          week_num: int,
                          season_id: int,
                          new_week: schemas.NewWeek) -> Week:
    week = Week(week_num=week_num, season_id=season_id, **new_week.model_dump())
    db.add(week)
    await db.flush()
    await db.refresh(week)
    return week

async def get_season_weeks(db: AsyncSession,
                           season_id: int):
    query = select(Week, Track, Car).where(Week.season_id == season_id) \
        .join(Track, Week.track_id == Track.id) \
        .join(Car, Week.car_id == Car.id) \
        .order_by(desc(Week.week_num))
    result = await db.execute(query)
    return result.all()

async def get_seasons_latest_week(db: AsyncSession,
                              season_id: int) -> Week:
    query = select(Week).where(Week.season_id == season_id).order_by(Week.week_num.desc()).limit(1)
    result = await db.execute(query)
    return result.scalars().first()

async def get_week(db: AsyncSession, week_id: int) -> schemas.WeekWithDetails:
    query = select(Week, Track, Car) \
        .join(Car, Week.car_id == Car.id) \
        .join(Track, Week.track_id == Track.id) \
        .where(Week.id == week_id)
    result = await db.execute(query)
    week, track, car = result.first()
    week_model = schemas.WeekWithDetails(
        week=WeekModel.model_validate(week),
        track=TrackModel.model_validate(track),
        car=CarModel.model_validate(car)
    )
    return week_model
