from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .init_db import engine


async def get_session() -> AsyncSession:
    return async_sessionmaker(engine, expire_on_commit=False)()
