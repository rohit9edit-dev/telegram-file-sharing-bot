from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class Subscription(BaseModel):
    """Subscription model (for future payment integration)"""
    user_id: int
    tier: str  # free, basic, pro, enterprise
    status: str = 'active'  # active, cancelled, expired
    payment_id: Optional[str] = None
    amount: Optional[float] = None
    currency: str = 'USD'
    billing_cycle: str = 'monthly'  # monthly, yearly
    starts_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Subscription':
        return cls(**data)