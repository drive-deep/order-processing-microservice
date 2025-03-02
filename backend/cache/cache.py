from abc import ABC, abstractmethod
from typing import Any, Optional

class CacheInterface(ABC):
    """Abstract interface for caching"""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from the cache"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: int = 3600) -> None:
        """Set a value in the cache with an expiration time"""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a key from the cache"""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear the entire cache"""
        pass
