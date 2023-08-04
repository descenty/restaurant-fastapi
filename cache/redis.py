from functools import wraps
import redis.asyncio as aioredis
from core.config import settings
import pickle
import logging
import asyncio

logging.basicConfig(level=logging.INFO)


def redis():
    return aioredis.from_url(settings.redis_url)


REDIS_AVAILABLE = False


async def check_redis():
    global REDIS_AVAILABLE
    try:
        REDIS_AVAILABLE = await redis().ping()
    except Exception as e:
        logging.error(f"Redis unavailable: {e}")


asyncio.get_event_loop().run_until_complete(check_redis())


def cached(key: str, **c_kwargs):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not REDIS_AVAILABLE:
                return await func(*args, **kwargs)
            key_format = key.format(**kwargs)
            cache = redis()
            if data := await cache.get(key_format):
                logging.info(f"get cache by key: {key_format}")
                return pickle.loads(data)
            else:
                result = await func(*args, **kwargs)
                await cache.set(key_format, pickle.dumps(result), **c_kwargs)
                logging.info(f"set cache by key: {key_format}")
                return result

        return wrapper

    return decorator


def invalidate(key: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not REDIS_AVAILABLE:
                return await func(*args, **kwargs)
            key_format = key.format(**kwargs)
            cache = redis()
            result = await func(*args, **kwargs)
            await cache.delete(key_format)
            print(f"invalidate cache by key: {key_format}")
            return result

        return wrapper

    return decorator
