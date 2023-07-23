from sqlalchemy.ext.asyncio import (
    create_async_engine,
)
from ..core.config import settings


engine = create_async_engine(settings.postgres_uri, echo=True)
