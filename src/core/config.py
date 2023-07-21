from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    CORS_ALLOW_ORIGINS: List[str] = ["http://localhost"]


settings = Settings()
