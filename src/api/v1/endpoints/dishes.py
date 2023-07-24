from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from models import Dish, Submenu
from schemas.dish import DishDTO, DishCreate
from uuid import UUID

router = APIRouter()


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[DishDTO]
)
async def get_all(
    menu_id: UUID,
    submenu_id: str,
    session: AsyncSession = Depends(get_session),
):
    return [
        DishDTO.model_validate(dish, from_attributes=True)
        for dish in (
            await session.scalars(
                select(Dish)
                .join(Submenu)
                .where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
            )
        )
    ]


@router.get(
    "/{menu_id}/submenus/{submenu_id}/dishes/{id}", response_model=DishDTO
)
async def get(
    menu_id: UUID,
    submenu_id: UUID,
    id: UUID,
    session: AsyncSession = Depends(get_session),
):
    if dish := (
        await session.scalars(
            select(Dish)
            .join(Submenu)
            .where(
                Submenu.menu_id == menu_id,
                Submenu.id == submenu_id,
                Dish.id == id,
            )
        )
    ).first():
        return DishDTO.model_validate(dish, from_attributes=True)
    raise HTTPException(status_code=404, detail="dish not found")


@router.post(
    "/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=DishDTO,
    status_code=201,
)
async def create(
    menu_id: UUID,
    submenu_id: UUID,
    dish_create: DishCreate,
    session: AsyncSession = Depends(get_session),
):
    if not (
        await session.scalars(
            select(Submenu).where(
                Submenu.menu_id == menu_id, Submenu.id == submenu_id
            )
        )
    ).first():
        raise HTTPException(status_code=404, detail="submenu not found")
    dish = Dish(submenu_id=submenu_id, **dish_create.model_dump())
    session.add(dish)
    await session.commit()
    await session.refresh(dish)
    return DishDTO.model_validate(dish, from_attributes=True)


@router.patch(
    "/{menu_id}/submenus/{submenu_id}/dishes/{id}", response_model=DishDTO
)
async def update(
    menu_id: UUID,
    submenu_id: UUID,
    id: UUID,
    dish_create: DishCreate,
    session: AsyncSession = Depends(get_session),
):
    if dish := (
        await session.scalars(
            select(Dish)
            .join(Submenu)
            .where(
                Submenu.menu_id == menu_id,
                Submenu.id == submenu_id,
                Dish.id == id,
            )
        )
    ).first():
        for var, value in dish_create.model_dump().items():
            setattr(dish, var, value)
        await session.commit()
        await session.refresh(dish)
        return DishDTO.model_validate(dish, from_attributes=True)
    raise HTTPException(status_code=404, detail="dish not found")


@router.delete(
    "/{menu_id}/submenus/{submenu_id}/dishes/{id}", response_model=DishDTO
)
async def delete(
    menu_id: UUID,
    submenu_id: UUID,
    id: UUID,
    session: AsyncSession = Depends(get_session),
):
    if dish := (
        await session.scalars(
            select(Dish).where(
                Submenu.menu_id == menu_id,
                Submenu.id == submenu_id,
                Dish.id == id,
            )
        )
    ).first():
        await session.delete(dish)
        await session.commit()
        return DishDTO.model_validate(dish, from_attributes=True)
    raise HTTPException(status_code=404, detail="dish not found")
