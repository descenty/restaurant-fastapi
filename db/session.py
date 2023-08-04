from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from .init_db import engine
from typing import (
    Any,
    AsyncGenerator,
    Annotated,
    Awaitable,
    Callable,
    Coroutine,
)
from fastapi import Depends


async def get_session() -> AsyncSession:
    return async_sessionmaker(engine, expire_on_commit=False)()

    # async with async_sessionmaker(
    #     engine, expire_on_commit=False
    # )() as async_session:
    #     yield async_session

    # try:
    #     yield async_session
    # finally:
    #     await async_session.commit()
    #     await async_session.close()


def db_session(func):
    async def wrapper(*args, **kwargs):
        async with async_sessionmaker(
            engine, expire_on_commit=False
        )() as session:
            return await func(*args, **kwargs, session=session)

    return wrapper


DBSession = Annotated[AsyncSession, Depends(get_session)]
