from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class User(BaseModel):
    """User model"""
    user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = 'user'  # user, admin, banned
    tier: str = 'free'  # free, basic, pro, enterprise
    is_banned: bool = False
    total_files: int = 0
    total_size: int = 0  # bytes
    total_downloads: int = 0
    last_active: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MongoDB"""
        data = self.model_dump()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create from MongoDB document"""
        return cls(**data)