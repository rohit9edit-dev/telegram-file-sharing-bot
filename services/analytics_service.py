from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from cache.redis_client import redis_client
from cache.keys import stats_key, global_stats_key
from utils.constants import CACHE_TTL_USER

class AnalyticsService:
    """Service for analytics and statistics"""
    
    def __init__(self, db):
        self.db = db
    
    async def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        # Try cache first
        cache_key = stats_key(user_id)
        cached = await redis_client.get(cache_key)
        if cached:
            return cached
        
        # Calculate from database
        user_doc = await self.db.users.find_one({'user_id': user_id})
        if not user_doc:
            return {}
        
        file_count = await self.db.files.count_documents({
            'user_id': user_id,
            'is_deleted': False
        })
        
        active_links = await self.db.links.count_documents({
            'user_id': user_id,
            'status': 'active'
        })
        
        total_downloads = await self.db.access_logs.count_documents({
            'user_id': user_id,
            'success': True
        })
        
        stats = {
            'total_files': file_count,
            'total_size': user_doc.get('total_size', 0),
            'active_links': active_links,
            'total_downloads': total_downloads,
            'member_since': user_doc.get('created_at'),
            'tier': user_doc.get('tier', 'free')
        }
        
        # Cache for 1 hour
        await redis_client.set(cache_key, stats, CACHE_TTL_USER)
        
        return stats
    
    async def get_global_stats(self) -> Dict[str, Any]:
        """Get global platform statistics"""
        # Try cache first
        cache_key = global_stats_key()
        cached = await redis_client.get(cache_key)
        if cached:
            return cached
        
        # Calculate from database
        stats = await self.calculate_global_stats()
        
        # Cache for 6 hours
        await redis_client.set(cache_key, stats, 21600)
        
        return stats
    
    async def calculate_global_stats(self) -> Dict[str, Any]:
        """Calculate global statistics from database"""
        total_users = await self.db.users.count_documents({})
        total_files = await self.db.files.count_documents({'is_deleted': False})
        active_links = await self.db.links.count_documents({'status': 'active'})
        total_downloads = await self.db.access_logs.count_documents({'success': True})
        
        # Calculate total storage
        pipeline = [
            {'$match': {'is_deleted': False}},
            {'$group': {'_id': None, 'total': {'$sum': '$file_size'}}}
        ]
        result = await self.db.files.aggregate(pipeline).to_list(1)
        total_size = result[0]['total'] if result else 0
        
        return {
            'total_users': total_users,
            'total_files': total_files,
            'total_size': total_size,
            'active_links': active_links,
            'total_downloads': total_downloads,
            'updated_at': datetime.utcnow()
        }
    
    async def update_global_stats(self):
        """Update global stats cache"""
        stats = await self.calculate_global_stats()
        cache_key = global_stats_key()
        await redis_client.set(cache_key, stats, 21600)
    
    async def get_file_analytics(self, file_id: str) -> Dict[str, Any]:
        """Get analytics for a specific file"""
        file_doc = await self.db.files.find_one({'file_id': file_id})
        if not file_doc:
            return {}
        
        link_count = await self.db.links.count_documents({'file_id': file_id})
        download_count = await self.db.access_logs.count_documents({
            'file_id': file_id,
            'success': True
        })
        
        return {
            'file_name': file_doc.get('file_name'),
            'file_size': file_doc.get('file_size'),
            'link_count': link_count,
            'download_count': download_count,
            'created_at': file_doc.get('created_at')
        }
    
    async def get_popular_files(self, limit: int = 10):
        """Get most downloaded files"""
        files = await self.db.files.find(
            {'is_deleted': False}
        ).sort('download_count', -1).limit(limit).to_list(limit)
        
        return files

class AnalyticsServiceFactory:
    """Factory for creating analytics service"""
    _instance = None
    
    @classmethod
    def create(cls, db):
        if cls._instance is None:
            cls._instance = AnalyticsService(db)
        return cls._instance

analytics_service = None