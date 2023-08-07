from uuid import UUID

from pydantic import BaseModel


class SubmenuDTO(BaseModel):
    id: UUID
    title: str
    description: str
    menu_id: UUID
    dishes_count: int = 0


class SubmenuCreate(BaseModel):
    title: str
    description: str
