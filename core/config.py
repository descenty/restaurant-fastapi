from typing import List

from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    url: str = "redis://:qweasdzxc@descenty.ru:6379"
    default_ttl: int = 3600  # 1 hour


class Settings(BaseSettings):
    app_title: str = "restaurant-fastapi"
    postgres_async_uri: str = (
        "postgresql+asyncpg://postgres:qweasdzxc@localhost:5432/restaurant"
    )
    cors_allow_origins: List[str] = ["http://localhost"]
    redis: RedisSettings = RedisSettings()


settings = Settings()
