from datetime import datetime
from typing import Optional, List
from database.models.file import File

class FileQueries:
    """File database queries"""
    
    def __init__(self, db):
        self.collection = db.files
    
    async def create_file(self, file: File) -> bool:
        """Create new file record"""
        try:
            await self.collection.insert_one(file.to_dict())
            return True
        except Exception as e:
            print(f"Error creating file: {e}")
            return False
    
    async def get_file(self, file_id: str) -> Optional[File]:
        """Get file by ID"""
        doc = await self.collection.find_one({'file_id': file_id, 'is_deleted': False})
        if doc:
            doc.pop('_id', None)
            return File.from_dict(doc)
        return None
    
    async def get_user_files(self, user_id: int, skip: int = 0, limit: int = 50) -> List[File]:
        """Get all files for a user"""
        cursor = self.collection.find(
            {'user_id': user_id, 'is_deleted': False}
        ).sort('created_at', -1).skip(skip).limit(limit)
        
        files = []
        async for doc in cursor:
            doc.pop('_id', None)
            files.append(File.from_dict(doc))
        return files
    
    async def search_files(self, user_id: int, query: str) -> List[File]:
        """Search files by name"""
        cursor = self.collection.find({
            'user_id': user_id,
            'is_deleted': False,
            'file_name': {'$regex': query, '$options': 'i'}
        }).sort('created_at', -1).limit(20)
        
        files = []
        async for doc in cursor:
            doc.pop('_id', None)
            files.append(File.from_dict(doc))
        return files
    
    async def update_file(self, file_id: str, updates: dict) -> bool:
        """Update file"""
        try:
            updates['updated_at'] = datetime.utcnow()
            result = await self.collection.update_one(
                {'file_id': file_id},
                {'$set': updates}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating file: {e}")
            return False
    
    async def delete_file(self, file_id: str) -> bool:
        """Soft delete file"""
        return await self.update_file(file_id, {'is_deleted': True})
    
    async def increment_download_count(self, file_id: str) -> bool:
        """Increment file download count"""
        try:
            await self.collection.update_one(
                {'file_id': file_id},
                {'$inc': {'download_count': 1}}
            )
            return True
        except Exception as e:
            print(f"Error incrementing download count: {e}")
            return False
    
    async def get_user_file_count(self, user_id: int) -> int:
        """Get total file count for user"""
        return await self.collection.count_documents({
            'user_id': user_id,
            'is_deleted': False
        })
    
    async def get_user_total_size(self, user_id: int) -> int:
        """Get total size of user files"""
        pipeline = [
            {'$match': {'user_id': user_id, 'is_deleted': False}},
            {'$group': {'_id': None, 'total': {'$sum': '$file_size'}}}
        ]
        result = await self.collection.aggregate(pipeline).to_list(1)
        return result[0]['total'] if result else 0