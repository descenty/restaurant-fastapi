from sqlalchemy.ext.asyncio import (
    create_async_engine,
)
from core.config import settings
from models.base import Base


engine = create_async_engine(settings.postgres_uri, echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
