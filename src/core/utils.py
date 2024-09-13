from typing import Type, TypeVar, List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar('T', bound=BaseModel)

def to_pydantic(model: Type[T], instance) -> T:
    return model.model_validate(instance)

def to_pydantic_list(model: Type[T], instances: List) -> List[T]:
    return [model.model_validate(instance) for instance in instances]