from pydantic import BaseModel
from src.cars.models import CarCategory

class NewCar(BaseModel):
    car_name: str
    car_category: CarCategory
    iracing_car_id: int = None
    iracing_car_picture: str = None
    garage61_car_id: int = None