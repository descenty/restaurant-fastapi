from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy import delete, exists, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.redis import cached, invalidate
from models import Dish, Menu, Submenu
from schemas.submenu import SubmenuCreate, SubmenuDTO


class SubmenuRepository:
    def __init__(self, background_tasks: BackgroundTasks):
        self.background_tasks = background_tasks

    @invalidate(
        ['menus', 'menus-cascade', 'menus-{menu_id}', 'menus-{menu_id}-submenus']
    )
    async def create(
        self,
        menu_id: UUID,
        submenu_create: SubmenuCreate,
        session: AsyncSession,
    ) -> SubmenuDTO | None:
        return (
            next(
                SubmenuDTO.model_validate(submenu, from_attributes=True)
                for submenu, in (
                    await session.execute(
                        insert(Submenu)
                        .values(submenu_create.model_dump() | {'menu_id': menu_id})
                        .returning(Submenu)
                    )
                )
            )
            if (
                await session.execute(select(exists().where(Menu.id == menu_id)))
            ).scalar()
            else None
        )

    @cached('menus-{menu_id}-submenus')
    async def read_all(
        self,
        menu_id: UUID,
        session: AsyncSession,
    ) -> list[SubmenuDTO]:
        return [
            SubmenuDTO.model_validate(submenu, from_attributes=True)
            for submenu in await session.execute(
                select(
                    Submenu.id,
                    Submenu.title,
                    Submenu.description,
                    Submenu.menu_id,
                    func.count(Dish.id).label('dishes_count'),
                )
                .outerjoin(Dish, onclause=Submenu.id == Dish.submenu_id)
                .where(Submenu.menu_id == menu_id)
                .group_by(Submenu.id)
            )
        ]

    @cached('menus-{menu_id}-submenus-{id}')
    async def read(
        self,
        menu_id: UUID,
        id: UUID,
        session: AsyncSession,
    ) -> SubmenuDTO | None:
        return next(
            (
                SubmenuDTO.model_validate(submenu, from_attributes=True)
                for submenu in await session.execute(
                    select(
                        Submenu.id,
                        Submenu.title,
                        Submenu.description,
                        Submenu.menu_id,
                        func.count(Dish.id).label('dishes_count'),
                    )
                    .outerjoin(Dish, onclause=Submenu.id == Dish.submenu_id)
                    .where(Submenu.menu_id == menu_id, Submenu.id == id)
                    .group_by(Submenu.id)
                )
            ),
            None,
        )

    @invalidate(
        [
            'menus',
            'menus-cascade',
            'menus-{menu_id}',
            'menus-{menu_id}-submenus',
            'menus-{menu_id}-submenus-{id}*',
        ]
    )
    async def update(
        self,
        menu_id: UUID,
        id: UUID,
        submenu_create: SubmenuCreate,
        session: AsyncSession,
    ) -> SubmenuDTO | None:
        return next(
            (
                SubmenuDTO.model_validate(
                    submenu.__dict__
                    | {
                        'dishes_count': dishes_count,
                    }
                )
                for (submenu,), (dishes_count, _) in zip(
                    await session.execute(
                        update(Submenu)
                        .where(Submenu.menu_id == menu_id, Submenu.id == id)
                        .values(submenu_create.model_dump() | {'menu_id': menu_id})
                        .returning(Submenu)
                    ),
                    await session.execute(
                        select(
                            func.count(Dish.id),
                            Submenu.id,
                        )
                        .outerjoin(Dish, onclause=Submenu.id == Dish.submenu_id)
                        .where(Submenu.id == id)
                        .group_by(Submenu.id)
                    ),
                )
            ),
            None,
        )

    @invalidate(
        [
            'menus',
            'menus-cascade',
            'menus-{menu_id}',
            'menus-{menu_id}-submenus',
            'menus-{menu_id}-submenus-{id}*',
        ]
    )
    async def delete(
        self,
        menu_id: UUID,
        id: UUID,
        session: AsyncSession,
    ) -> UUID | None:
        return next(
            (
                deleted_id
                for deleted_id, in await session.execute(
                    delete(Submenu)
                    .where(Submenu.menu_id == menu_id, Submenu.id == id)
                    .returning(Submenu.id)
                )
            ),
            None,
        )
