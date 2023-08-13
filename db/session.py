from asyncio.tasks import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
)

from .init_db import engine

async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
AsyncScopedSession = async_scoped_session(
    async_session_factory,
    scopefunc=current_task,
)


def get_session() -> AsyncSession:
    return AsyncScopedSession()
