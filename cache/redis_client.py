import redis.asyncio as redis
from typing import Optional, Any
import json
from config import config

class RedisClient:
    """Redis cache client"""
    
    def __init__(self):
        self.client: Optional[redis.Redis] = None
        self.connected = False
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.client = redis.Redis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                password=config.REDIS_PASSWORD,
                db=config.REDIS_DB,
                decode_responses=True
            )
            await self.client.ping()
            self.connected = True
            print("✅ Redis connected successfully")
            return True
        except Exception as e:
            print(f"⚠️  Redis connection failed: {e}")
            print("ℹ️  Continuing without cache...")
            self.connected = False
            return False
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.client:
            await self.client.close()
            print("🔒 Redis disconnected")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.connected:
            return None
        try:
            value = await self.client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL"""
        if not self.connected:
            return False
        try:
            await self.client.setex(
                key,
                ttl,
                json.dumps(value)
            )
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.connected:
            return False
        try:
            await self.client.delete(key)
            return True
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.connected:
            return False
        try:
            return await self.client.exists(key) > 0
        except Exception as e:
            return False
    
    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment counter"""
        if not self.connected:
            return 0
        try:
            return await self.client.incrby(key, amount)
        except Exception as e:
            print(f"Redis increment error: {e}")
            return 0
    
    async def expire(self, key: str, ttl: int) -> bool:
        """Set expiry on existing key"""
        if not self.connected:
            return False
        try:
            return await self.client.expire(key, ttl)
        except Exception as e:
            return False

# Global Redis instance
redis_client = RedisClient()