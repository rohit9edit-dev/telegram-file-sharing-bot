from datetime import datetime
from typing import Optional, List
from database.models.link import Link

class LinkQueries:
    """Link database queries"""
    
    def __init__(self, db):
        self.collection = db.links
    
    async def create_link(self, link: Link) -> bool:
        """Create new download link"""
        try:
            await self.collection.insert_one(link.to_dict())
            return True
        except Exception as e:
            print(f"Error creating link: {e}")
            return False
    
    async def get_link(self, link_id: str) -> Optional[Link]:
        """Get link by ID"""
        doc = await self.collection.find_one({'link_id': link_id})
        if doc:
            doc.pop('_id', None)
            return Link.from_dict(doc)
        return None
    
    async def get_user_links(self, user_id: int, active_only: bool = False) -> List[Link]:
        """Get all links for a user"""
        query = {'user_id': user_id}
        if active_only:
            query['status'] = 'active'
        
        cursor = self.collection.find(query).sort('created_at', -1).limit(50)
        links = []
        async for doc in cursor:
            doc.pop('_id', None)
            links.append(Link.from_dict(doc))
        return links
    
    async def get_file_links(self, file_id: str) -> List[Link]:
        """Get all links for a file"""
        cursor = self.collection.find({'file_id': file_id})
        links = []
        async for doc in cursor:
            doc.pop('_id', None)
            links.append(Link.from_dict(doc))
        return links
    
    async def update_link(self, link_id: str, updates: dict) -> bool:
        """Update link"""
        try:
            result = await self.collection.update_one(
                {'link_id': link_id},
                {'$set': updates}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating link: {e}")
            return False
    
    async def revoke_link(self, link_id: str) -> bool:
        """Revoke link"""
        return await self.update_link(link_id, {
            'status': 'revoked',
            'revoked_at': datetime.utcnow()
        })
    
    async def increment_access(self, link_id: str) -> bool:
        """Increment link access count"""
        try:
            now = datetime.utcnow()
            await self.collection.update_one(
                {'link_id': link_id},
                {
                    '$inc': {'access_count': 1},
                    '$set': {'last_accessed_at': now},
                    '$setOnInsert': {'first_accessed_at': now}
                },
                upsert=False
            )
            return True
        except Exception as e:
            print(f"Error incrementing access: {e}")
            return False
    
    async def set_first_access(self, link_id: str) -> bool:
        """Set first access time if not already set"""
        try:
            await self.collection.update_one(
                {'link_id': link_id, 'first_accessed_at': None},
                {'$set': {'first_accessed_at': datetime.utcnow()}}
            )
            return True
        except Exception as e:
            return False
    
    async def cleanup_expired_links(self) -> int:
        """Mark expired links as expired"""
        try:
            result = await self.collection.update_many(
                {
                    'status': 'active',
                    'expires_at': {'$lt': datetime.utcnow()}
                },
                {'$set': {'status': 'expired'}}
            )
            return result.modified_count
        except Exception as e:
            print(f"Error cleaning up links: {e}")
            return 0
    
    async def get_active_link_count(self, user_id: Optional[int] = None) -> int:
        """Get count of active links"""
        query = {'status': 'active'}
        if user_id:
            query['user_id'] = user_id
        return await self.collection.count_documents(query)