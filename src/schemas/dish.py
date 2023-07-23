from pydantic import BaseModel


class DishCreate(BaseModel):
    title: str
    description: str
