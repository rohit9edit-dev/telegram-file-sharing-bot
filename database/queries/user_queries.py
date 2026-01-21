from datetime import datetime
from typing import Optional, Dict, Any
from database.models.user import User

class UserQueries:
    """User database queries"""
    
    def __init__(self, db):
        self.collection = db.users
    
    async def create_user(self, user: User) -> bool:
        """Create new user"""
        try:
            await self.collection.insert_one(user.to_dict())
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        doc = await self.collection.find_one({'user_id': user_id})
        if doc:
            doc.pop('_id', None)
            return User.from_dict(doc)
        return None
    
    async def get_or_create_user(self, user_id: int, **kwargs) -> User:
        """Get user or create if not exists"""
        user = await self.get_user(user_id)
        if not user:
            user = User(user_id=user_id, **kwargs)
            await self.create_user(user)
        return user
    
    async def update_user(self, user_id: int, updates: Dict[str, Any]) -> bool:
        """Update user"""
        try:
            updates['updated_at'] = datetime.utcnow()
            result = await self.collection.update_one(
                {'user_id': user_id},
                {'$set': updates}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    async def increment_stats(self, user_id: int, field: str, value: int = 1) -> bool:
        """Increment user statistics"""
        try:
            await self.collection.update_one(
                {'user_id': user_id},
                {'$inc': {field: value}}
            )
            return True
        except Exception as e:
            print(f"Error incrementing stats: {e}")
            return False
    
    async def ban_user(self, user_id: int) -> bool:
        """Ban user"""
        return await self.update_user(user_id, {'is_banned': True, 'role': 'banned'})
    
    async def unban_user(self, user_id: int) -> bool:
        """Unban user"""
        return await self.update_user(user_id, {'is_banned': False, 'role': 'user'})
    
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list:
        """Get all users with pagination"""
        cursor = self.collection.find({}).skip(skip).limit(limit)
        users = []
        async for doc in cursor:
            doc.pop('_id', None)
            users.append(User.from_dict(doc))
        return users
    
    async def get_user_count(self) -> int:
        """Get total user count"""
        return await self.collection.count_documents({})
    
    async def get_active_users(self, days: int = 30) -> int:
        """Get count of active users in last N days"""
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(days=days)
        return await self.collection.count_documents({
            'last_active': {'$gte': cutoff}
        })