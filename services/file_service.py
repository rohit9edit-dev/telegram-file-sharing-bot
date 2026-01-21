from typing import Optional, BinaryIO
from datetime import datetime
from database.models.file import File
from database.queries.file_queries import FileQueries
from database.queries.user_queries import UserQueries
from utils.hash import generate_file_id, generate_file_hash
from utils.validators import sanitize_filename
from config import config

class FileService:
    """Service for file operations"""
    
    def __init__(self, db):
        self.file_queries = FileQueries(db)
        self.user_queries = UserQueries(db)
    
    async def create_file_record(self, 
                                  user_id: int,
                                  telegram_file_id: str,
                                  telegram_message_id: int,
                                  file_name: str,
                                  file_size: int,
                                  file_type: str,
                                  mime_type: Optional[str] = None,
                                  is_encrypted: bool = False) -> Optional[File]:
        """Create a new file record"""
        try:
            file_id = generate_file_id()
            sanitized_name = sanitize_filename(file_name)
            
            file = File(
                file_id=file_id,
                user_id=user_id,
                telegram_file_id=telegram_file_id,
                telegram_message_id=telegram_message_id,
                file_name=sanitized_name,
                file_size=file_size,
                file_type=file_type,
                mime_type=mime_type,
                is_encrypted=is_encrypted
            )
            
            success = await self.file_queries.create_file(file)
            if success:
                # Update user stats
                await self.user_queries.increment_stats(user_id, 'total_files')
                await self.user_queries.increment_stats(user_id, 'total_size', file_size)
                return file
            
            return None
        except Exception as e:
            print(f"Error creating file record: {e}")
            return None
    
    async def get_file(self, file_id: str) -> Optional[File]:
        """Get file by ID"""
        return await self.file_queries.get_file(file_id)
    
    async def get_user_files(self, user_id: int, skip: int = 0, limit: int = 50):
        """Get user's files"""
        return await self.file_queries.get_user_files(user_id, skip, limit)
    
    async def search_files(self, user_id: int, query: str):
        """Search user's files"""
        return await self.file_queries.search_files(user_id, query)
    
    async def delete_file(self, file_id: str, user_id: int) -> bool:
        """Delete file"""
        file = await self.get_file(file_id)
        if not file or file.user_id != user_id:
            return False
        
        success = await self.file_queries.delete_file(file_id)
        if success:
            # Update user stats
            await self.user_queries.increment_stats(user_id, 'total_files', -1)
            await self.user_queries.increment_stats(user_id, 'total_size', -file.file_size)
        
        return success
    
    async def increment_download(self, file_id: str) -> bool:
        """Increment file download count"""
        return await self.file_queries.increment_download_count(file_id)
    
    async def get_user_storage_stats(self, user_id: int) -> dict:
        """Get user storage statistics"""
        file_count = await self.file_queries.get_user_file_count(user_id)
        total_size = await self.file_queries.get_user_total_size(user_id)
        
        return {
            'file_count': file_count,
            'total_size': total_size
        }