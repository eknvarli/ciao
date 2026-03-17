import json
from typing import Any, Optional, Callable
import redis.asyncio as redis
from functools import wraps

from app.core.config import settings

redis_client: Optional[redis.Redis] = None

async def init_redis():
    global redis_client
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def get_redis():
    return redis_client

async def close_redis():
    if redis_client:
        await redis_client.close()

def cache_response(ttl: int = 300):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not redis_client:
                return await func(*args, **kwargs)
                
            key_parts = [func.__name__]
            for arg in args:
                if isinstance(arg, (str, int, float, bool)):
                     key_parts.append(str(arg))
            for k, v in sorted(kwargs.items()):
                 if isinstance(v, (str, int, float, bool)):
                     key_parts.append(f"{k}:{v}")
            
            cache_key = ":".join(key_parts)
            
            try:
                cached_value = await redis_client.get(cache_key)
                if cached_value:
                    return json.loads(cached_value)
            except Exception as e:
                print(f"Redis get error: {e}")
                
            result = await func(*args, **kwargs)
            
            try:
                if result is not None:
                     await redis_client.setex(cache_key, ttl, json.dumps(result))
            except Exception as e:
                print(f"Redis set error: {e}")
                
            return result
        return wrapper
    return decorator
