from pydantic import BaseModel
from datetime import datetime


from src.cars.models import CarCategory

class NewCar(BaseModel):
    car_name: str
    car_category: CarCategory
    iracing_car_id: int = None
    iracing_car_picture: str = None
    garage61_car_id: int = None
    
class CarModel(BaseModel):
    id: int
    car_name: str
    car_category: CarCategory
    iracing_car_id: int
    iracing_car_picture: str
    garage61_car_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True