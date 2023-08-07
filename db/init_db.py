from sqlalchemy.ext.asyncio import create_async_engine

from core.config import settings
from models.base import BaseModel

postgres_url = ''.join(
    [
        'postgresql+asyncpg://',
        f'{settings.postgres.user}:',
        f'{settings.postgres.password}@',
        f'{settings.postgres.host}:',
        f'{settings.postgres.port}',
        f'/{settings.postgres.db}',
    ]
)

engine = create_async_engine(postgres_url)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
