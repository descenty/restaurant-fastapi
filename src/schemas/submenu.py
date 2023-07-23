from pydantic import BaseModel


class SubmenuCreate(BaseModel):
    title: str
    description: str
