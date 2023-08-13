from uuid import UUID

from pydantic import BaseModel, field_validator

from schemas.dish import DishDTO


class SubmenuDTO(BaseModel):
    id: UUID
    title: str
    description: str
    menu_id: UUID
    dishes_count: int = 0


class SubmenuCascadeDTO(SubmenuDTO):
    dishes: list[DishDTO] = []

    @field_validator('dishes', mode='before')
    def dishes_validator(cls, dishes: list[DishDTO]):
        return [dish for dish in dishes if dish is not None]


class SubmenuCreate(BaseModel):
    title: str
    description: str
