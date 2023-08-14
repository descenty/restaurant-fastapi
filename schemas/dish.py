from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, model_validator


class DishDTO(BaseModel):
    id: UUID
    title: str
    description: str
    price: Decimal
    actual_price: Decimal = Decimal(0)
    discount: Decimal = Decimal(0)
    submenu_id: UUID

    @model_validator(mode='after')
    def validator(self):
        self.actual_price = max(
            Decimal(0), Decimal(round(self.price * (1 - self.discount), 2))
        )
        return self


class DishCreate(BaseModel):
    title: str
    description: str
    price: Decimal
    discount: Decimal = Decimal(0)
