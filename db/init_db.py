from sqlalchemy.ext.asyncio import create_async_engine
from core.config import settings
from models.base import BaseModel


engine = create_async_engine(settings.postgres_async_uri)  # , echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
