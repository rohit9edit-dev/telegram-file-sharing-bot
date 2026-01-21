from typing import Optional
from datetime import datetime, timedelta
from database.models.link import Link
from database.models.access_log import AccessLog
from database.queries.link_queries import LinkQueries
from database.queries.user_queries import UserQueries
from utils.hash import generate_link_id
from utils.validators import calculate_expiry
from config import config

class LinkService:
    """Service for download link operations"""
    
    def __init__(self, db):
        self.link_queries = LinkQueries(db)
        self.user_queries = UserQueries(db)
        self.db = db
    
    async def create_link(self,
                          file_id: str,
                          user_id: int,
                          expiry_days: Optional[int] = None,
                          max_access: Optional[int] = None,
                          self_destruct: bool = False,
                          self_destruct_after: Optional[int] = None,
                          password: Optional[str] = None) -> Optional[Link]:
        """Create a new download link"""
        try:
            link_id = generate_link_id()
            
            # Calculate expiry
            expires_at = None
            if expiry_days:
                expires_at = calculate_expiry(expiry_days)
            elif config.LINK_EXPIRY_DAYS > 0:
                expires_at = calculate_expiry(config.LINK_EXPIRY_DAYS)
            
            link = Link(
                link_id=link_id,
                file_id=file_id,
                user_id=user_id,
                expires_at=expires_at,
                max_access=max_access,
                self_destruct=self_destruct,
                self_destruct_after=self_destruct_after,
                password=password
            )
            
            success = await self.link_queries.create_link(link)
            return link if success else None
        except Exception as e:
            print(f"Error creating link: {e}")
            return None
    
    async def get_link(self, link_id: str) -> Optional[Link]:
        """Get link by ID"""
        return await self.link_queries.get_link(link_id)
    
    async def validate_link_access(self, link: Link) -> tuple[bool, Optional[str]]:
        """Validate if link can be accessed"""
        if not link.is_accessible():
            if link.status == 'revoked':
                return False, "❌ This link has been revoked."
            elif link.status == 'expired':
                return False, "❌ This link has expired."
            elif link.expires_at and datetime.utcnow() > link.expires_at:
                # Mark as expired
                await self.link_queries.update_link(link.link_id, {'status': 'expired'})
                return False, "❌ This link has expired."
            elif link.max_access and link.access_count >= link.max_access:
                return False, "❌ This link has reached its maximum access limit."
            elif link.self_destruct and link.first_accessed_at and link.self_destruct_after:
                elapsed = (datetime.utcnow() - link.first_accessed_at).total_seconds()
                if elapsed > link.self_destruct_after:
                    return False, "❌ This link has self-destructed."
            else:
                return False, "❌ This link is not accessible."
        
        return True, None
    
    async def access_link(self, link_id: str, user_id: Optional[int] = None) -> tuple[bool, Optional[str]]:
        """Record link access"""
        link = await self.get_link(link_id)
        if not link:
            return False, "❌ Link not found."
        
        # Validate access
        valid, error = await self.validate_link_access(link)
        if not valid:
            return False, error
        
        # Set first access time if needed
        if not link.first_accessed_at:
            await self.link_queries.set_first_access(link_id)
        
        # Increment access count
        await self.link_queries.increment_access(link_id)
        
        # Log access
        access_log = AccessLog(
            link_id=link_id,
            file_id=link.file_id,
            user_id=user_id,
            success=True
        )
        await self.db.access_logs.insert_one(access_log.to_dict())
        
        return True, None
    
    async def revoke_link(self, link_id: str, user_id: int) -> bool:
        """Revoke a link"""
        link = await self.get_link(link_id)
        if not link or link.user_id != user_id:
            return False
        
        return await self.link_queries.revoke_link(link_id)
    
    async def get_user_links(self, user_id: int, active_only: bool = False):
        """Get user's links"""
        return await self.link_queries.get_user_links(user_id, active_only)
    
    async def get_file_links(self, file_id: str):
        """Get all links for a file"""
        return await self.link_queries.get_file_links(file_id)