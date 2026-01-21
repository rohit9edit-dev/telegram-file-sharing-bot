from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class Referral(BaseModel):
    """Referral model (for future referral program)"""
    referrer_id: int
    referred_id: int
    status: str = 'pending'  # pending, completed, rewarded
    reward_amount: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    rewarded_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Referral':
        return cls(**data)