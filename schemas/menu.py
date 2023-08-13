from uuid import UUID

from pydantic import BaseModel, field_validator

from schemas.submenu import SubmenuCascadeDTO


class MenuDTO(BaseModel):
    id: UUID
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0


class MenuCascadeDTO(MenuDTO):
    submenus: list[SubmenuCascadeDTO] = []

    @field_validator('submenus', mode='before')
    def dishes_validator(cls, submenus: list[SubmenuCascadeDTO]):
        return [submenu for submenu in submenus if submenu is not None]


class MenuCreate(BaseModel):
    title: str
    description: str
