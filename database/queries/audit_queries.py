from datetime import datetime
from database.models.audit import AuditLog
from typing import List, Optional

class AuditQueries:
    """Audit log database queries"""
    
    def __init__(self, db):
        self.collection = db.audit_logs
    
    async def log_action(self, audit: AuditLog) -> bool:
        """Log an action"""
        try:
            await self.collection.insert_one(audit.to_dict())
            return True
        except Exception as e:
            print(f"Error logging action: {e}")
            return False
    
    async def get_user_logs(self, user_id: int, limit: int = 50) -> List[AuditLog]:
        """Get audit logs for a user"""
        cursor = self.collection.find(
            {'user_id': user_id}
        ).sort('timestamp', -1).limit(limit)
        
        logs = []
        async for doc in cursor:
            doc.pop('_id', None)
            logs.append(AuditLog.from_dict(doc))
        return logs
    
    async def get_resource_logs(self, resource_id: str, limit: int = 50) -> List[AuditLog]:
        """Get audit logs for a resource"""
        cursor = self.collection.find(
            {'resource_id': resource_id}
        ).sort('timestamp', -1).limit(limit)
        
        logs = []
        async for doc in cursor:
            doc.pop('_id', None)
            logs.append(AuditLog.from_dict(doc))
        return logs
    
    async def get_action_logs(self, action: str, days: int = 7) -> List[AuditLog]:
        """Get logs for specific action in last N days"""
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        cursor = self.collection.find({
            'action': action,
            'timestamp': {'$gte': cutoff}
        }).sort('timestamp', -1)
        
        logs = []
        async for doc in cursor:
            doc.pop('_id', None)
            logs.append(AuditLog.from_dict(doc))
        return logs