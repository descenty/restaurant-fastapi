from fastapi import Depends
from sqlalchemy import select, delete, insert, update, exists
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from models import Submenu, Dish
from schemas.dish import DishDTO, DishCreate
from uuid import UUID
from repository.crud_repository import CRUDRepository


class DishRepository(CRUDRepository):
    @staticmethod
    async def create(
        menu_id: UUID,
        submenu_id: UUID,
        dish_create: DishCreate,
        session: AsyncSession = Depends(get_session),
    ) -> DishDTO | None:
        return (
            next(
                DishDTO.model_validate(dish, from_attributes=True)
                for dish, in (
                    await session.execute(
                        insert(Dish)
                        .values(
                            dish_create.model_dump()
                            | {"submenu_id": submenu_id}
                        )
                        .returning(Dish)
                    )
                )
            )
            if (
                await session.execute(
                    select(
                        exists().where(
                            Submenu.menu_id == menu_id,
                            Submenu.id == submenu_id,
                        )
                    )
                )
            ).scalar()
            else None
        )

    @staticmethod
    async def read_all(
        menu_id: UUID,
        submenu_id: UUID,
        session: AsyncSession = Depends(get_session),
    ) -> list[DishDTO]:
        return [
            DishDTO.model_validate(dish, from_attributes=True)
            for dish, in await session.execute(
                select(Dish)
                .join(Submenu, onclause=Dish.submenu_id == Submenu.id)
                .where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
            )
        ]

    @staticmethod
    async def read(
        menu_id: UUID,
        submenu_id: UUID,
        id: UUID,
        session: AsyncSession = Depends(get_session),
    ) -> DishDTO | None:
        return next(
            (
                DishDTO.model_validate(dish, from_attributes=True)
                for dish, in await session.execute(
                    select(Dish)
                    .join(Submenu, onclause=Dish.submenu_id == Submenu.id)
                    .where(
                        Submenu.menu_id == menu_id,
                        Submenu.id == submenu_id,
                        Dish.id == id,
                    )
                )
            ),
            None,
        )

    @staticmethod
    async def update(
        menu_id: UUID,
        submenu_id: UUID,
        id: UUID,
        dish_create: DishCreate,
        session: AsyncSession = Depends(get_session),
    ) -> DishDTO | None:
        return (
            next(
                DishDTO.model_validate(dish, from_attributes=True)
                for dish, in (
                    await session.execute(
                        update(Dish)
                        .where(Dish.submenu_id == submenu_id, Dish.id == id)
                        .values(dish_create.model_dump())
                        .returning(Dish)
                    )
                )
            )
            if (
                await session.execute(
                    select(
                        exists().where(
                            Submenu.menu_id == menu_id,
                            Submenu.id == submenu_id,
                        )
                    )
                )
            ).scalar()
            else None
        )

    @staticmethod
    async def delete(
        menu_id: UUID,
        submenu_id: UUID,
        id: UUID,
        session: AsyncSession = Depends(get_session),
    ) -> UUID | None:
        return (
            next(
                (
                    deleted_id
                    for deleted_id, in await session.execute(
                        delete(Dish)
                        .where(Dish.submenu_id == submenu_id, Dish.id == id)
                        .returning(Dish.id)
                    )
                ),
                None,
            )
            if (
                await session.execute(
                    select(
                        exists().where(
                            Submenu.menu_id == menu_id,
                            Submenu.id == submenu_id,
                        )
                    )
                )
            ).scalar()
            else None
        )
