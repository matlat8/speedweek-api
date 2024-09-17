from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy.ext.asyncio
from src.auth.users import User, current_active_user
from src.core.db import get_db_session
from src.cars.schemas import NewCar
from src.cars.crud import create_new_car, get_all_cars

cars = APIRouter(prefix="/cars")

@cars.get("")
async def rt_get_cars(db: AsyncSession = Depends(get_db_session), user: User = Depends(current_active_user)): # 
    # search via car name or dont search if None
    cars = await get_all_cars(db)
    return {"data": cars}

@cars.post("")
async def rt_create_new_car(car_info: NewCar, db: AsyncSession = Depends(get_db_session), user: User = Depends(current_active_user)):
    new_car = await create_new_car(db=db, new_car=car_info)
    await db.commit()
    return {"data": new_car}