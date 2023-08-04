from fastapi import Depends
from db.session import get_session
from schemas.menu import MenuCreate, MenuDTO
from repository.menu import MenuRepository
from uuid import UUID


class MenuService:
    def __init__(self, repository: MenuRepository = Depends(MenuRepository)):
        self.repository = repository

    async def get_all(self) -> list[MenuDTO]:
        async with await get_session() as session:
            return await self.repository.read_all(session)

    async def get(self, id: UUID) -> MenuDTO | None:
        async with await get_session() as session:
            return await self.repository.read(id, session)

    async def create(self, menu_create: MenuCreate) -> MenuDTO:
        async with await get_session() as session:
            menu = await MenuRepository.create(menu_create, session)
            await session.commit()
        return menu

    async def update(
        self, id: UUID, menu_create: MenuCreate
    ) -> MenuDTO | None:
        async with await get_session() as session:
            menu = await self.repository.update(id, menu_create, session)
            await session.commit()
        return menu

    async def delete(self, id: UUID) -> UUID | None:
        async with await get_session() as session:
            menu = await self.repository.delete(id, session)
            await session.commit()
        return menu
