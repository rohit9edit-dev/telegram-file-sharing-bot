"""Self-destruct plugin for time-limited files"""
from pyrogram import Client
from datetime import datetime, timedelta
import asyncio

class SelfDestructPlugin:
    """Plugin for self-destructing files"""
    
    def __init__(self, client: Client):
        self.client = client
        self.active_tasks = {}
    
    async def schedule_destruct(self, link_id: str, file_id: str, seconds: int):
        """Schedule file destruction after specified seconds"""
        print(f"Scheduled self-destruct for {link_id} in {seconds}s")
        
        # Create async task
        task = asyncio.create_task(self._destruct_after(link_id, file_id, seconds))
        self.active_tasks[link_id] = task
    
    async def _destruct_after(self, link_id: str, file_id: str, seconds: int):
        """Destroy file after countdown"""
        await asyncio.sleep(seconds)
        
        try:
            from database.connection import get_database
            from database.queries.link_queries import LinkQueries
            
            db = await get_database()
            link_queries = LinkQueries(db)
            
            # Update link status to expired
            await link_queries.update_link(link_id, {
                'status': 'expired',
                'revoked_at': datetime.utcnow()
            })
            
            print(f"💥 Self-destructed: {link_id}")
            
        except Exception as e:
            print(f"Error in self-destruct: {e}")
        
        # Remove from active tasks
        self.active_tasks.pop(link_id, None)
    
    def cancel_destruct(self, link_id: str) -> bool:
        """Cancel scheduled destruction"""
        task = self.active_tasks.get(link_id)
        if task:
            task.cancel()
            self.active_tasks.pop(link_id, None)
            return True
        return False

# Global instance
self_destruct_plugin = None

def setup_plugin(app: Client):
    """Setup self-destruct plugin"""
    global self_destruct_plugin
    self_destruct_plugin = SelfDestructPlugin(app)
    print("✅ Self-destruct plugin initialized")

def get_plugin() -> SelfDestructPlugin:
    """Get plugin instance"""
    return self_destruct_plugin