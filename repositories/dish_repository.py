from uuid import UUID

from sqlalchemy import delete, exists, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.redis import cached, invalidate
from models import Dish, Submenu
from schemas.dish import DishCreate, DishDTO


class DishRepository:
    @invalidate(
        [
            'menus',
            'menus-{menu_id}',
            'menus-{menu_id}-submenus',
            'menus-{menu_id}-submenus-{submenu_id}',
            'menus-{menu_id}-submenus-{submenu_id}-dishes',
        ]
    )
    async def create(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        dish_create: DishCreate,
        session: AsyncSession,
    ) -> DishDTO | None:
        return (
            next(
                DishDTO.model_validate(dish, from_attributes=True)
                for dish, in (
                    await session.execute(
                        insert(Dish)
                        .values(dish_create.model_dump() | {'submenu_id': submenu_id})
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

    @cached('menus-{menu_id}-submenus-{submenu_id}-dishes')
    async def read_all(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        session: AsyncSession,
    ) -> list[DishDTO]:
        return [
            DishDTO.model_validate(dish, from_attributes=True)
            for dish, in await session.execute(
                select(Dish)
                .join(Submenu, onclause=Dish.submenu_id == Submenu.id)
                .where(Submenu.menu_id == menu_id, Submenu.id == submenu_id)
            )
        ]

    @cached('menus-{menu_id}-submenus-{submenu_id}-dishes-{id}')
    async def read(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        id: UUID,
        session: AsyncSession,
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

    @invalidate(
        [
            'menus',
            'menus-{menu_id}',
            'menus-{menu_id}-submenus',
            'menus-{menu_id}-submenus-{submenu_id}',
            'menus-{menu_id}-submenus-{submenu_id}-dishes',
            'menus-{menu_id}-submenus-{submenu_id}-dishes-{id}*',
        ]
    )
    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        id: UUID,
        dish_create: DishCreate,
        session: AsyncSession,
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

    @invalidate(
        [
            'menus',
            'menus-{menu_id}',
            'menus-{menu_id}-submenus',
            'menus-{menu_id}-submenus-{submenu_id}',
            'menus-{menu_id}-submenus-{submenu_id}-dishes',
            'menus-{menu_id}-submenus-{submenu_id}-dishes-{id}*',
        ]
    )
    async def delete(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        id: UUID,
        session: AsyncSession,
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
