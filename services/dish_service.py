from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from db.session import get_session
from repositories.dish_repository import DishRepository
from schemas.dish import DishCreate, DishDTO


class DishService:
    def __init__(self, repository: DishRepository):
        self.repository = repository

    async def get_all(self, menu_id: UUID, submenu_id: UUID) -> list[DishDTO]:
        async with await get_session() as session:
            return await self.repository.read_all(menu_id, submenu_id, session)

    async def get(self, menu_id: UUID, submenu_id: UUID, id: UUID) -> DishDTO | None:
        async with await get_session() as session:
            return await self.repository.read(menu_id, submenu_id, id, session)

    async def create(
        self, menu_id: UUID, submenu_id: UUID, dish_create: DishCreate
    ) -> DishDTO | None:
        async with await get_session() as session:
            submenu = await self.repository.create(
                menu_id, submenu_id, dish_create, session
            )
            await session.commit()
        return submenu

    async def update(
        self,
        menu_id: UUID,
        submenu_id: UUID,
        id: UUID,
        dish_create: DishCreate,
    ) -> DishDTO | None:
        async with await get_session() as session:
            submenu = await self.repository.update(
                menu_id, submenu_id, id, dish_create, session
            )
            await session.commit()
        return submenu

    async def delete(self, menu_id: UUID, submenu_id: UUID, id: UUID) -> UUID | None:
        async with await get_session() as session:
            deleted_id = await self.repository.delete(menu_id, submenu_id, id, session)
            await session.commit()
        return deleted_id


@lru_cache
def dish_service(repository: DishRepository = Depends(DishRepository)) -> DishService:
    return DishService(repository)
