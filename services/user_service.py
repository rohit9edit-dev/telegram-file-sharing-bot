from datetime import datetime
from typing import Optional
from database.models.user import User
from database.queries.user_queries import UserQueries
from config import config

class UserService:
    """Service for user operations"""
    
    def __init__(self, db):
        self.user_queries = UserQueries(db)
    
    async def get_or_create_user(self, 
                                  user_id: int,
                                  username: Optional[str] = None,
                                  first_name: Optional[str] = None,
                                  last_name: Optional[str] = None) -> User:
        """Get existing user or create new one"""
        user = await self.user_queries.get_user(user_id)
        
        if not user:
            # Check if user is admin
            role = 'admin' if user_id in config.ADMIN_IDS else 'user'
            
            user = User(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            await self.user_queries.create_user(user)
        else:
            # Update user info if changed
            updates = {}
            if username and username != user.username:
                updates['username'] = username
            if first_name and first_name != user.first_name:
                updates['first_name'] = first_name
            if last_name and last_name != user.last_name:
                updates['last_name'] = last_name
            
            if updates:
                await self.user_queries.update_user(user_id, updates)
        
        return user
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return await self.user_queries.get_user(user_id)
    
    async def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        if user_id in config.ADMIN_IDS:
            return True
        
        user = await self.get_user(user_id)
        return user and user.role == 'admin'
    
    async def is_banned(self, user_id: int) -> bool:
        """Check if user is banned"""
        user = await self.get_user(user_id)
        return user and user.is_banned
    
    async def ban_user(self, user_id: int) -> bool:
        """Ban a user"""
        return await self.user_queries.ban_user(user_id)
    
    async def unban_user(self, user_id: int) -> bool:
        """Unban a user"""
        return await self.user_queries.unban_user(user_id)
    
    async def update_activity(self, user_id: int) -> bool:
        """Update user's last active time"""
        return await self.user_queries.update_user(user_id, {
            'last_active': datetime.utcnow()
        })
    
    async def get_all_users(self, skip: int = 0, limit: int = 100):
        """Get all users"""
        return await self.user_queries.get_all_users(skip, limit)
    
    async def get_user_stats(self, user_id: int) -> dict:
        """Get user statistics"""
        user = await self.get_user(user_id)
        if not user:
            return {}
        
        return {
            'total_files': user.total_files,
            'total_size': user.total_size,
            'total_downloads': user.total_downloads,
            'tier': user.tier,
            'member_since': user.created_at
        }