from typing import Any, Callable, Coroutine, Awaitable
from fastapi import APIRouter, Depends, HTTPException, Response, 
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from models import Menu, Submenu, Dish
from schemas.menu import MenuDTO, MenuCreate
import logging
from uuid import UUID
from repository.menu import MenuRepository

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("", response_model=list[MenuDTO])
async def get_all(
    menus: list[MenuDTO] = Depends(MenuRepository.read_all),
):
    return menus


@router.get("/{id}", response_model=MenuDTO)
async def get(menu: MenuDTO | None = Depends(MenuRepository.read)):
    if menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return menu


@router.post("", response_model=MenuDTO, status_code=201)
async def create(
    menu_create: MenuCreate, session: AsyncSession = Depends(get_session)
):
    menu = Menu(**menu_create.model_dump())
    session.add(menu)
    await session.commit()
    await session.refresh(menu)
    return MenuDTO.model_validate(menu, from_attributes=True)


@router.patch("/{id}", response_model=MenuDTO)
async def update(
    id: UUID,
    menu_create: MenuCreate,
    session: AsyncSession = Depends(get_session),
):
    if row := (
        await session.execute(
            select(
                Menu,
                func.count(func.distinct(Submenu.id)),
                func.count(Dish.id),
            )
            .join(Submenu, onclause=Menu.id == Submenu.menu_id, isouter=True)
            .join(Dish, onclause=Submenu.id == Dish.submenu_id, isouter=True)
            .where(Menu.id == id)
            .group_by(Menu.id)
        )
    ).first():
        menu, submenus_count, dishes_count = row
        for var, value in menu_create.model_dump().items():
            setattr(menu, var, value)
        await session.commit()
        await session.refresh(menu)
        return MenuDTO.model_validate(
            menu.__dict__
            | {"submenus_count": submenus_count, "dishes_count": dishes_count}
        )
    raise HTTPException(status_code=404, detail="menu not found")


@router.delete("/{id}", response_model=MenuDTO)
async def delete(id: UUID, session: AsyncSession = Depends(get_session)):
    if row := (
        await session.execute(
            select(
                Menu,
                func.count(func.distinct(Submenu.id)),
                func.count(Dish.id),
            )
            .join(Submenu, onclause=Menu.id == Submenu.menu_id, isouter=True)
            .join(Dish, onclause=Submenu.id == Dish.submenu_id, isouter=True)
            .where(Menu.id == id)
            .group_by(Menu.id)
        )
    ).first():
        menu, submenus_count, dishes_count = row
        await session.delete(menu)
        await session.commit()
        return MenuDTO.model_validate(
            menu.__dict__
            | {"submenus_count": submenus_count, "dishes_count": dishes_count}
        )
    raise HTTPException(status_code=404, detail="menu not found")
