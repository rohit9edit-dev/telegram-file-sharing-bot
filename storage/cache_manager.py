"""Cache manager for frequently accessed data"""
from typing import Optional, Any
from cache.redis_client import redis_client
from cache.keys import file_key, link_key, user_key
from utils.constants import CACHE_TTL_FILE, CACHE_TTL_LINK, CACHE_TTL_USER
import json

class CacheManager:
    """Manage caching of frequently accessed data"""
    
    def __init__(self):
        self.redis = redis_client
    
    async def cache_file(self, file_id: str, file_data: dict, ttl: int = CACHE_TTL_FILE) -> bool:
        """Cache file data"""
        key = file_key(file_id)
        return await self.redis.set(key, file_data, ttl)
    
    async def get_cached_file(self, file_id: str) -> Optional[dict]:
        """Get cached file data"""
        key = file_key(file_id)
        return await self.redis.get(key)
    
    async def cache_link(self, link_id: str, link_data: dict, ttl: int = CACHE_TTL_LINK) -> bool:
        """Cache link data"""
        key = link_key(link_id)
        return await self.redis.set(key, link_data, ttl)
    
    async def get_cached_link(self, link_id: str) -> Optional[dict]:
        """Get cached link data"""
        key = link_key(link_id)
        return await self.redis.get(key)
    
    async def invalidate_link(self, link_id: str) -> bool:
        """Invalidate link cache"""
        key = link_key(link_id)
        return await self.redis.delete(key)
    
    async def cache_user(self, user_id: int, user_data: dict, ttl: int = CACHE_TTL_USER) -> bool:
        """Cache user data"""
        key = user_key(user_id)
        return await self.redis.set(key, user_data, ttl)
    
    async def get_cached_user(self, user_id: int) -> Optional[dict]:
        """Get cached user data"""
        key = user_key(user_id)
        return await self.redis.get(key)
    
    async def invalidate_user(self, user_id: int) -> bool:
        """Invalidate user cache"""
        key = user_key(user_id)
        return await self.redis.delete(key)
    
    async def clear_all(self) -> bool:
        """Clear all cache (use with caution)"""
        if self.redis.connected:
            try:
                await self.redis.client.flushdb()
                return True
            except Exception as e:
                print(f"Error clearing cache: {e}")
                return False
        return False

cache_manager = CacheManager()