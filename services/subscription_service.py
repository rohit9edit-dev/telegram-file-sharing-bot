"""Subscription service (for future payment integration)"""
from typing import Optional
from datetime import datetime, timedelta
from database.models.subscription import Subscription
from utils.constants import TIER_FREE, TIER_LIMITS

class SubscriptionService:
    """Service for subscription management (placeholder for future use)"""
    
    def __init__(self, db):
        self.db = db
        self.collection = db.subscriptions
    
    async def get_user_subscription(self, user_id: int) -> Optional[Subscription]:
        """Get user's active subscription"""
        doc = await self.collection.find_one({
            'user_id': user_id,
            'status': 'active'
        })
        if doc:
            doc.pop('_id', None)
            return Subscription.from_dict(doc)
        return None
    
    async def get_user_tier(self, user_id: int) -> str:
        """Get user's subscription tier"""
        subscription = await self.get_user_subscription(user_id)
        return subscription.tier if subscription else TIER_FREE
    
    async def get_tier_limits(self, tier: str) -> dict:
        """Get limits for a tier"""
        return TIER_LIMITS.get(tier, TIER_LIMITS[TIER_FREE])
    
    async def check_limit(self, user_id: int, limit_type: str, current_value: int) -> bool:
        """Check if user is within limits"""
        tier = await self.get_user_tier(user_id)
        limits = await self.get_tier_limits(tier)
        
        max_value = limits.get(limit_type, 0)
        if max_value == -1:  # Unlimited
            return True
        
        return current_value < max_value
    
    async def create_subscription(self, subscription: Subscription) -> bool:
        """Create a new subscription (placeholder)"""
        try:
            await self.collection.insert_one(subscription.to_dict())
            return True
        except Exception as e:
            print(f"Error creating subscription: {e}")
            return False
    
    async def cancel_subscription(self, user_id: int) -> bool:
        """Cancel user's subscription"""
        result = await self.collection.update_one(
            {'user_id': user_id, 'status': 'active'},
            {'$set': {
                'status': 'cancelled',
                'cancelled_at': datetime.utcnow()
            }}
        )
        return result.modified_count > 0