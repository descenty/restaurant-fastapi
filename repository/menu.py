from fastapi import Depends
from sqlalchemy import select, func, delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from models import Menu, Submenu, Dish
from schemas.menu import MenuDTO, MenuCreate
from uuid import UUID
from repository.crud_repository import CRUDRepository


class MenuRepository(CRUDRepository):
    @staticmethod
    async def create(
        menu_create: MenuCreate, session: AsyncSession = Depends(get_session)
    ) -> MenuDTO:
        return next(
            MenuDTO.model_validate(menu, from_attributes=True)
            for menu, in await session.execute(
                insert(Menu).values(menu_create.model_dump()).returning(Menu)
            )
        )

    @staticmethod
    async def read_all(
        session: AsyncSession = Depends(get_session),
    ) -> list[MenuDTO]:
        return [
            MenuDTO.model_validate(
                menu.__dict__
                | {
                    "submenus_count": submenus_count,
                    "dishes_count": dishes_count,
                },
            )
            for menu, submenus_count, dishes_count in await session.execute(
                select(
                    Menu,
                    func.count(func.distinct(Submenu.id)),
                    func.count(Dish.id),
                )
                .outerjoin(Submenu, onclause=Menu.id == Submenu.menu_id)
                .outerjoin(Dish, onclause=Submenu.id == Dish.submenu_id)
                .group_by(Menu.id)
            )
        ]

    @staticmethod
    async def read(
        id: UUID, session: AsyncSession = Depends(get_session)
    ) -> MenuDTO | None:
        return next(
            (
                MenuDTO.model_validate(
                    menu.__dict__
                    | {
                        "submenus_count": submenus_count,
                        "dishes_count": dishes_count,
                    }
                )
                for menu, submenus_count, dishes_count in await session.execute(
                    select(
                        Menu,
                        func.count(func.distinct(Submenu.id)),
                        func.count(Dish.id),
                    )
                    .outerjoin(Submenu, onclause=Menu.id == Submenu.menu_id)
                    .outerjoin(Dish, onclause=Submenu.id == Dish.submenu_id)
                    .where(Menu.id == id)
                    .group_by(Menu.id)
                )
            ),
            None,
        )

    @staticmethod
    async def update(
        id: UUID,
        menu_create: MenuCreate,
        session: AsyncSession = Depends(get_session),
    ) -> MenuDTO | None:
        return next(
            (
                MenuDTO.model_validate(
                    menu.__dict__
                    | {
                        "submenus_count": submenus_count,
                        "dishes_count": dishes_count,
                    }
                )
                for (menu,), (submenus_count, dishes_count, _) in zip(
                    await session.execute(
                        update(Menu)
                        .where(Menu.id == id)
                        .values(menu_create.model_dump())
                        .returning(Menu)
                    ),
                    await session.execute(
                        select(
                            func.count(func.distinct(Submenu.id)),
                            func.count(Dish.id),
                            Menu.id,
                        )
                        .outerjoin(
                            Submenu, onclause=Menu.id == Submenu.menu_id
                        )
                        .outerjoin(
                            Dish, onclause=Submenu.id == Dish.submenu_id
                        )
                        .where(Menu.id == id)
                        .group_by(Menu.id)
                    ),
                )
            ),
            None,
        )

    @staticmethod
    async def delete(
        id: UUID, session: AsyncSession = Depends(get_session)
    ) -> UUID | None:
        return next(
            (
                deleted_id
                for deleted_id, in await session.execute(
                    delete(Menu).where(Menu.id == id).returning(Menu.id)
                )
            ),
            None,
        )
