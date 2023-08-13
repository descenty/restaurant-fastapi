from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from db.session import get_session
from repositories.menu_repository import MenuRepository
from schemas.menu import MenuCascadeDTO, MenuCreate, MenuDTO


class MenuService:
    def __init__(self, repository):
        self.repository = repository

    async def get_all(self) -> list[MenuDTO]:
        async with get_session() as session:
            return await self.repository.read_all(session)

    async def get_all_cascade(self) -> list[MenuCascadeDTO]:
        async with get_session() as session:
            return await self.repository.read_all_cascade(session)

    async def get(self, id: UUID) -> MenuDTO | None:
        async with get_session() as session:
            return await self.repository.read(id, session)

    async def create(self, menu_create: MenuCreate) -> MenuDTO:
        async with get_session() as session:
            menu = await self.repository.create(menu_create, session)
            await session.commit()
        return menu

    async def update(self, id: UUID, menu_create: MenuCreate) -> MenuDTO | None:
        async with get_session() as session:
            menu = await self.repository.update(id, menu_create, session)
            await session.commit()
        return menu

    async def delete(self, id: UUID) -> UUID | None:
        async with get_session() as session:
            deleted_id = await self.repository.delete(id, session)
            await session.commit()
        return deleted_id


@lru_cache
def menu_service(repository: MenuRepository = Depends(MenuRepository)) -> MenuService:
    return MenuService(repository)
