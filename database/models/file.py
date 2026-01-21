from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class File(BaseModel):
    """File model"""
    file_id: str
    user_id: int
    telegram_file_id: str
    telegram_message_id: int
    file_name: str
    file_size: int  # bytes
    file_type: str  # document, video, audio, photo, etc.
    mime_type: Optional[str] = None
    file_hash: Optional[str] = None
    is_encrypted: bool = False
    is_deleted: bool = False
    download_count: int = 0
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for MongoDB"""
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'File':
        """Create from MongoDB document"""
        return cls(**data)