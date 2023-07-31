from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from .init_db import engine
from typing import AsyncGenerator, Annotated
from fastapi import Depends


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(engine, expire_on_commit=False)()
    try:
        yield async_session
    finally:
        await async_session.commit()
        await async_session.close()


DBSession = Annotated[AsyncSession, Depends(get_session)]
