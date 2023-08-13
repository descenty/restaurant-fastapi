from uuid import UUID

from fastapi import BackgroundTasks
from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from cache.redis import cached, invalidate
from models import Dish, Menu, Submenu
from schemas.menu import MenuCascadeDTO, MenuCreate, MenuDTO


class MenuRepository:
    def __init__(self, background_tasks: BackgroundTasks):
        self.background_tasks = background_tasks

    @invalidate(['menus', 'menus-cascade'])
    async def create(
        self,
        menu_create: MenuCreate,
        session: AsyncSession,
    ) -> MenuDTO:
        return next(
            MenuDTO.model_validate(menu, from_attributes=True)
            for menu, in await session.execute(
                insert(Menu).values(menu_create.model_dump()).returning(Menu)
            )
        )

    @cached('menus')
    async def read_all(
        self,
        session: AsyncSession,
    ) -> list[MenuDTO]:
        return [
            MenuDTO.model_validate(menu, from_attributes=True)
            for menu in await session.execute(
                select(
                    Menu.id,
                    Menu.title,
                    Menu.description,
                    func.count(func.distinct(Submenu.id)).label('submenus_count'),
                    func.count(Dish.id).label('dishes_count'),
                )
                .outerjoin(Submenu, onclause=Menu.id == Submenu.menu_id)
                .outerjoin(Dish, onclause=Submenu.id == Dish.submenu_id)
                .group_by(Menu.id)
            )
        ]

    @cached('menus-cascade')
    async def read_all_cascade(self, session: AsyncSession) -> list[MenuCascadeDTO]:
        return [
            MenuCascadeDTO.model_validate(menu, from_attributes=True)
            for menu, in await session.execute(
                select(Menu).options(
                    selectinload(Menu.submenus).options(selectinload(Submenu.dishes))
                )
            )
        ]

    @cached('menus-{id}')
    async def read(self, id: UUID, session: AsyncSession) -> MenuDTO | None:
        return next(
            (
                MenuDTO.model_validate(menu, from_attributes=True)
                for menu in await session.execute(
                    select(
                        Menu.id,
                        Menu.title,
                        Menu.description,
                        func.count(func.distinct(Submenu.id)).label('submenus_count'),
                        func.count(Dish.id).label('dishes_count'),
                    )
                    .outerjoin(Submenu, onclause=Menu.id == Submenu.menu_id)
                    .outerjoin(Dish, onclause=Submenu.id == Dish.submenu_id)
                    .where(Menu.id == id)
                    .group_by(Menu.id)
                )
            ),
            None,
        )

    @invalidate(['menus', 'menus-cascade', 'menus-{id}*'])
    async def update(
        self,
        id: UUID,
        menu_create: MenuCreate,
        session: AsyncSession,
    ) -> MenuDTO | None:
        return next(
            (
                MenuDTO.model_validate(
                    menu.__dict__
                    | {
                        'submenus_count': submenus_count,
                        'dishes_count': dishes_count,
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
                        .outerjoin(Submenu, onclause=Menu.id == Submenu.menu_id)
                        .outerjoin(Dish, onclause=Submenu.id == Dish.submenu_id)
                        .where(Menu.id == id)
                        .group_by(Menu.id)
                    ),
                )
            ),
            None,
        )

    @invalidate(['menus', 'menus-cascade', 'menus-{id}*'])
    async def delete(self, id: UUID, session: AsyncSession) -> UUID | None:
        return next(
            (
                deleted_id
                for deleted_id, in await session.execute(
                    delete(Menu).where(Menu.id == id).returning(Menu.id)
                )
            ),
            None,
        )
