from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class AccessLog(BaseModel):
    """Access log model for tracking downloads"""
    link_id: str
    file_id: str
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    accessed_at: datetime = Field(default_factory=datetime.utcnow)
    success: bool = True
    error_message: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AccessLog':
        return cls(**data)