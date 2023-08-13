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
        self.submenus_count = len(self.submenus)
        for submenu in self.submenus:
            submenu.dishes_count = len(submenu.dishes)
            for dish in submenu.dishes:
                self.dishes_count += 1
                dish.price = dish.price * (1 + dish.discount)
        return self


class MenuCreate(BaseModel):
    title: str
    description: str
