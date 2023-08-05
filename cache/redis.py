from functools import lru_cache, wraps
from typing import Any
import redis.asyncio as aioredis
from core.config import settings
import pickle
import logging
import asyncio

logger = logging.getLogger("uvicorn")


def redis() -> aioredis.Redis:
    return aioredis.from_url(settings.redis.url)


class RedisClient:
    is_available: bool = False

    def __init__(self):
        asyncio.create_task(self.check_redis())

    async def check_redis(self):
        while True:
            try:
                self.is_available = await redis().ping()
                logger.info("Redis is available")
            except Exception as e:
                logger.error(f"Redis is unavailable: {e}")
            await asyncio.sleep(60)

    async def get(self, key: str, **kwargs) -> Any | None:
        try:
            if self.is_available:
                if data := await redis().get(key, **kwargs):
                    logger.info(f"get cache by key: {key}")
                    return data
                else:
                    logger.info(f"cache not found by key: {key}")
        except Exception as e:
            logger.error(f"Redis get error: {e}")

    async def set(
        self, key: str, value, ex: int = settings.redis.default_ttl, **kwargs
    ) -> Any | None:
        try:
            if self.is_available:
                logger.info(f"set cache by key: {key}")
                await redis().set(
                    key,
                    value,
                    ex=ex,
                )
        except Exception as e:
            logger.error(f"Redis set error: {e}")

    async def delete(self, keys: str | list[str], **kwargs) -> Any | None:
        try:
            if self.is_available:
                r = redis()
                for key in keys if isinstance(keys, list) else [keys]:
                    for key_match in await r.keys(key):
                        await r.delete(key_match)
                        logger.info(
                            f"invalidate cache by key: {key_match.decode()}"
                        )
        except Exception as e:
            logger.error(f"Redis delete error: {e}")


@lru_cache()
def redis_client():
    return RedisClient()


def cached(key: str, **cache_kwargs):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            rclient = redis_client()
            if not rclient.is_available:
                return await func(*args, **kwargs)
            key_format = key.format(**kwargs)
            if data := await rclient.get(key_format):
                return pickle.loads(data)

            result = await func(*args, **kwargs)
            await rclient.set(key_format, pickle.dumps(result), **cache_kwargs)
            return result

        return wrapper

    return decorator


def invalidate(keys: list[str] | str, **cache_kwargs):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            rclient = redis_client()
            result = await func(*args, **kwargs)
            keys_format = (
                [key.format(**kwargs) for key in keys]
                if isinstance(keys, list)
                else [keys.format(**kwargs)]
            )
            await rclient.delete(keys_format, **cache_kwargs)
            return result

        return wrapper

    return decorator
