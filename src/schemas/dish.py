from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel


class DishDTO(BaseModel):
    id: UUID
    title: str
    description: str
    price: Decimal
    submenu_id: UUID


class DishCreate(BaseModel):
    title: str
    description: str
    price: Decimal
