from pyrogram import Client
from pyrogram.types import Message
from typing import Callable
from functools import wraps
from config import config
from cache.redis_client import redis_client
from cache.keys import rate_limit_key
import time

def admin_only(func: Callable):
    """Decorator to restrict handler to admins only"""
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        user_id = message.from_user.id
        if user_id not in config.ADMIN_IDS:
            await message.reply_text("❌ You don't have permission to use this command.")
            return
        return await func(client, message)
    return wrapper

def rate_limit(max_calls: int, period: int):
    """Rate limiting decorator"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(client: Client, message: Message):
            user_id = message.from_user.id
            key = rate_limit_key(user_id, func.__name__)
            
            # Check rate limit
            count = await redis_client.get(key) or 0
            if count >= max_calls:
                await message.reply_text(
                    f"⚠️ Rate limit exceeded. Please wait before trying again."
                )
                return
            
            # Increment counter
            if count == 0:
                await redis_client.set(key, 1, period)
            else:
                await redis_client.increment(key)
            
            return await func(client, message)
        return wrapper
    return decorator

def check_banned(func: Callable):
    """Check if user is banned"""
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        from database.connection import get_database
        from database.queries.user_queries import UserQueries
        
        user_id = message.from_user.id
        db = await get_database()
        user_queries = UserQueries(db)
        user = await user_queries.get_user(user_id)
        
        if user and user.is_banned:
            await message.reply_text("❌ You are banned from using this bot.")
            return
        
        return await func(client, message)
    return wrapper

def track_activity(func: Callable):
    """Track user activity"""
    @wraps(func)
    async def wrapper(client: Client, message: Message):
        from datetime import datetime
        from database.connection import get_database
        from database.queries.user_queries import UserQueries
        
        user_id = message.from_user.id
        db = await get_database()
        user_queries = UserQueries(db)
        
        # Update last active time
        await user_queries.update_user(user_id, {
            'last_active': datetime.utcnow()
        })
        
        return await func(client, message)
    return wrapper