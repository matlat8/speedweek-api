from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from src.cars.models import Car
from src.cars.schemas import NewCar

async def create_new_car(db: AsyncSession, new_car: NewCar) -> Car:
    car = Car(**new_car.model_dump())
    db.add(car)
    await db.flush()
    await db.refresh(car)
    return car

async def get_all_cars(db: AsyncSession) -> List[Car]:
    query = select(Car)
    result = await db.execute(query)
    results = result.scalars().all()
    return results