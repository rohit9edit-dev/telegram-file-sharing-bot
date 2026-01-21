from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class Link(BaseModel):
    """Download link model"""
    link_id: str
    file_id: str
    user_id: int
    status: str = 'active'  # active, expired, revoked, used
    access_count: int = 0
    max_access: Optional[int] = None  # None = unlimited
    self_destruct: bool = False
    self_destruct_after: Optional[int] = None  # seconds after first access
    password: Optional[str] = None
    expires_at: Optional[datetime] = None
    first_accessed_at: Optional[datetime] = None
    last_accessed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    revoked_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MongoDB"""
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Link':
        """Create from MongoDB document"""
        return cls(**data)
    
    def is_accessible(self) -> bool:
        """Check if link is accessible"""
        if self.status != 'active':
            return False
        
        # Check expiry
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        
        # Check max access
        if self.max_access and self.access_count >= self.max_access:
            return False
        
        # Check self-destruct
        if self.self_destruct and self.first_accessed_at and self.self_destruct_after:
            elapsed = (datetime.utcnow() - self.first_accessed_at).total_seconds()
            if elapsed > self.self_destruct_after:
                return False
        
        return True