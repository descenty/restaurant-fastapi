from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from .init_db import engine
from typing import AsyncGenerator


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
