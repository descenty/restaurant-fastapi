from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = "restaurant-fastapi"
    postgres_async_uri: str = (
        "postgresql+asyncpg://postgres:qweasdzxc@localhost:5432/restaurant"
    )
    cors_allow_origins: List[str] = ["http://localhost"]

    # model_config = SettingsConfigDict(
    #     env_file=".env", env_file_encoding="utf-8"
    # )


settings = Settings()
