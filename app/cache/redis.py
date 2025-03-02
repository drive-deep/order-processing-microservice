import aioredis
import json
from typing import Any, Optional
from app.cache.cache import CacheInterface
from app.core.config import settings  # Load Redis configuration

class RedisCache(CacheInterface):
    """Redis implementation of the caching interface"""

    def __init__(self):
        self.redis = None

    async def init_cache(self):
        """Initialize Redis connection"""
        self.redis = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)

    async def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from Redis"""
        value = await self.redis.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: Any, expire: int = 3600) -> None:
        """Set a value in Redis with an expiration time"""
        await self.redis.setex(key, expire, json.dumps(value))

    async def delete(self, key: str) -> None:
        """Delete a key from Redis"""
        await self.redis.delete(key)

    async def clear(self) -> None:
        """Clear the entire Redis cache"""
        await self.redis.flushdb()

# Global RedisCache instance
redis_cache = RedisCache()

# Initialize Redis on app startup
async def init_redis():
    await redis_cache.init_cache()
