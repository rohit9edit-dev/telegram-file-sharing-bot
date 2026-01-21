from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class AuditLog(BaseModel):
    """Audit log model for tracking all actions"""
    user_id: int
    action: str  # upload, download, delete, revoke, ban, etc.
    resource_type: str  # file, link, user
    resource_id: str
    details: Dict[str, Any] = Field(default_factory=dict)
    ip_address: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AuditLog':
        return cls(**data)