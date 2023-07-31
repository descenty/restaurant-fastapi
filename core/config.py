from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "restaurant-fastapi"
    postgres_async_uri: str = (
        "postgresql+asyncpg://postgres:qweasdzxc@localhost:5432/restaurant"
    )
    cors_allow_origins: List[str] = ["http://localhost"]


settings = Settings()
