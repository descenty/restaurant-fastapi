from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from db.session import get_session
from repositories.submenu_repository import SubmenuRepository
from schemas.submenu import SubmenuCreate, SubmenuDTO


class SubmenuService:
    def __init__(self, repository: SubmenuRepository):
        self.repository = repository

    async def get_all(self, menu_id: UUID) -> list[SubmenuDTO]:
        async with await get_session() as session:
            return await self.repository.read_all(menu_id, session)

    async def get(self, menu_id: UUID, id: UUID) -> SubmenuDTO | None:
        async with await get_session() as session:
            return await self.repository.read(menu_id, id, session)

    async def create(
        self, menu_id: UUID, submenu_create: SubmenuCreate
    ) -> SubmenuDTO | None:
        async with await get_session() as session:
            submenu = await self.repository.create(menu_id, submenu_create, session)
            await session.commit()
        return submenu

    async def update(
        self, menu_id: UUID, id: UUID, submenu_create: SubmenuCreate
    ) -> SubmenuDTO | None:
        async with await get_session() as session:
            submenu = await self.repository.update(menu_id, id, submenu_create, session)
            await session.commit()
        return submenu

    async def delete(self, menu_id: UUID, id: UUID) -> UUID | None:
        async with await get_session() as session:
            deleted_id = await self.repository.delete(menu_id, id, session)
            await session.commit()
        return deleted_id


@lru_cache
def submenu_service(
    repository: SubmenuRepository = Depends(SubmenuRepository),
) -> SubmenuService:
    return SubmenuService(repository)
