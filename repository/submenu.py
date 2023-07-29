from fastapi import Depends
from sqlalchemy import select, func, delete, insert, update, exists
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from models import Menu, Submenu, Dish
from schemas.submenu import SubmenuDTO, SubmenuCreate
from uuid import UUID
from repository.crud_repository import CRUDRepository


class SubmenuRepository(CRUDRepository):
    @staticmethod
    async def create(
        menu_id: UUID,
        submenu_create: SubmenuCreate,
        session: AsyncSession = Depends(get_session),
    ) -> SubmenuDTO | None:
        return (
            [
                SubmenuDTO.model_validate(submenu, from_attributes=True)
                for submenu, in (
                    await session.execute(
                        insert(Submenu)
                        .values(
                            submenu_create.model_dump() | {"menu_id": menu_id}
                        )
                        .returning(Submenu)
                    )
                )
            ]
            if (
                await session.execute(
                    select(exists().where(Menu.id == menu_id))
                )
            ).scalar()
            else [None]
        )[0]

    @staticmethod
    async def read_all(
        menu_id: UUID,
        session: AsyncSession = Depends(get_session),
    ) -> list[SubmenuDTO]:
        return [
            SubmenuDTO.model_validate(
                submenu.__dict__
                | {
                    "dishes_count": dishes_count,
                },
            )
            for submenu, dishes_count in await session.execute(
                select(
                    Submenu,
                    func.count(Dish.id),
                )
                .outerjoin(Dish, onclause=Submenu.id == Dish.submenu_id)
                .where(Submenu.menu_id == menu_id)
                .group_by(Submenu.id)
            )
        ]

    @staticmethod
    async def read(
        menu_id: UUID, id: UUID, session: AsyncSession = Depends(get_session)
    ) -> SubmenuDTO | None:
        return (
            [
                SubmenuDTO.model_validate(
                    submenu.__dict__
                    | {
                        "dishes_count": dishes_count,
                    }
                )
                for submenu, dishes_count in await session.execute(
                    select(
                        Submenu,
                        func.count(Dish.id),
                    )
                    .outerjoin(Dish, onclause=Submenu.id == Dish.submenu_id)
                    .where(Submenu.menu_id == menu_id, Submenu.id == id)
                    .group_by(Submenu.id)
                )
            ]
            or [None]
        )[0]

    @staticmethod
    async def update(
        menu_id: UUID,
        id: UUID,
        submenu_create: SubmenuCreate,
        session: AsyncSession = Depends(get_session),
    ) -> SubmenuDTO | None:
        return (
            [
                SubmenuDTO.model_validate(
                    submenu.__dict__
                    | {
                        "dishes_count": dishes_count,
                    }
                )
                for submenu, in (
                    await session.execute(
                        update(Submenu)
                        .where(Submenu.menu_id == menu_id, Submenu.id == id)
                        .values(
                            submenu_create.model_dump() | {"menu_id": menu_id}
                        )
                        .returning(Submenu)
                    )
                )
                for dishes_count, _ in await session.execute(
                    select(
                        func.count(Dish.id),
                        Submenu.id,
                    )
                    .outerjoin(Dish, onclause=Submenu.id == Dish.submenu_id)
                    .where(Submenu.id == id)
                    .group_by(Submenu.id)
                )
            ]
            or [None]
        )[0]

    @staticmethod
    async def delete(
        menu_id: UUID, id: UUID, session: AsyncSession = Depends(get_session)
    ) -> SubmenuDTO | None:
        return (
            [
                SubmenuDTO.model_validate(
                    submenu.__dict__
                    | {
                        "dishes_count": dishes_count,
                    }
                )
                for dishes_count, _ in await session.execute(
                    select(
                        func.count(Dish.id),
                        Submenu.id,
                    )
                    .outerjoin(Dish, onclause=Submenu.id == Dish.submenu_id)
                    .where(Submenu.menu_id == menu_id, Submenu.id == id)
                    .group_by(Submenu.id)
                )
                for submenu, in await session.execute(
                    delete(Submenu)
                    .where(Submenu.menu_id == menu_id, Submenu.id == id)
                    .returning(Submenu)
                )
            ]
            or [None]
        )[0]
