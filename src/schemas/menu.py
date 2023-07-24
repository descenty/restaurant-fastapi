from uuid import UUID
from pydantic import BaseModel


class MenuDTO(BaseModel):
    id: UUID
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0


class MenuCreate(BaseModel):
    title: str
    description: str
