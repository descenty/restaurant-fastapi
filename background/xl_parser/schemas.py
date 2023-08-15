from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, model_validator

from schemas.dish import DishCreate
from schemas.menu import MenuCreate
from schemas.submenu import SubmenuCreate


class IDModel(BaseModel):
    id: int


class DishCascadeCreate(IDModel, DishCreate):
    @model_validator(mode='before')
    def validator(cls, row: tuple):
        id, title, description, price, discount = (
            row[0],
            row[1],
            row[2],
            row[3],
            (row[4] or 0.0),
        )
        assert isinstance(id, int) and id > 0, 'id must be positive integer'
        assert len(title) > 0, 'title must be non-empty string'
        assert len(description) > 0, 'description must be non-empty string'
        assert (
            isinstance(price, float) and (d_price := Decimal(price)) > 0
        ), 'price must be positive decimal'
        assert (
            isinstance(discount, float) and (d_discount := Decimal(discount)) >= 0
        ), 'discount must be non-negative decimal'
        return {
            'id': id,
            'title': title,
            'description': description,
            'price': d_price,
            'discount': d_discount,
        }


class SubmenuCascadeCreate(IDModel, SubmenuCreate):
    dishes: list[DishCascadeCreate] = []

    @model_validator(mode='before')
    def validator(cls, row: tuple):
        return MenuCascadeCreate.model_validate(row).model_dump()


class MenuCascadeCreate(IDModel, MenuCreate):
    submenus: list[SubmenuCascadeCreate] = []

    @model_validator(mode='before')
    def validator(cls, v: tuple | dict):
        if isinstance(v, dict):
            return v
        id, title, description = v[0], v[1], v[2]
        assert isinstance(id, int) and id > 0, 'id must be positive integer'
        assert len(title) > 0, 'title must be non-empty string'
        assert len(description) > 0, 'description must be non-empty string'
        return {'id': id, 'title': title, 'description': description}


class XLBinding(BaseModel):
    xl_id: int
    db_id: UUID


class XLSubmenuBinding(XLBinding):
    dishes: list[XLBinding] = []


class XLMenuBinding(XLBinding):
    submenus: list[XLSubmenuBinding] = []


class XLMenusBindings(BaseModel):
    menus: list[XLMenuBinding] = []
