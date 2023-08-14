from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, model_validator

from schemas.submenu import SubmenuCascadeDTO


class MenuDTO(BaseModel):
    id: UUID
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0


class MenuCascadeDTO(MenuDTO):
    submenus: list[SubmenuCascadeDTO] = []

    @model_validator(mode='after')
    def validator(self):
        self.submenus_count = 0
        self.dishes_count = 0
        for submenu in self.submenus:
            self.submenus_count += 1
            for dish in submenu.dishes:
                self.dishes_count += 1
                submenu.dishes_count += 1
                dish.actual_price = Decimal(
                    round(max(0, dish.price * (1 - dish.discount)), 2)
                )
        return self


class MenuCreate(BaseModel):
    title: str
    description: str
