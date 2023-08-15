from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseModel):
    host: str = 'localhost'
    port: int = 5432
    user: str = 'postgres'
    password: str = 'postgres'
    db: str = 'restaurant'


class RedisSettings(BaseModel):
    host: str = 'localhost'
    port: int = 6379
    password: str = ''
    default_ttl: int = 3600
    enabled: bool = True


class CelerySettings(BaseModel):
    broker: str = 'amqp://localhost:5672'
    backend: str = 'redis://localhost:6379'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter='_',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='allow',
    )
    app_url: str = 'http://localhost:8000'
    app_title: str = 'restaurant-fastapi'
    cors_allow_origins: list[str] = ['http://localhost']
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
    celery: CelerySettings = CelerySettings()
    menus_xl_path: str = 'admin/Menu.xlsx'


settings = Settings()
