from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

class BotScheduler:
    """Background task scheduler"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
    
    def start(self):
        """Start scheduler"""
        # Schedule cleanup tasks
        self.scheduler.add_job(
            self.cleanup_expired_links,
            'interval',
            hours=1,
            id='cleanup_links'
        )
        
        self.scheduler.add_job(
            self.update_analytics,
            'interval',
            hours=6,
            id='update_analytics'
        )
        
        self.scheduler.start()
        print("✅ Scheduler started")
    
    def stop(self):
        """Stop scheduler"""
        self.scheduler.shutdown()
        print("🛑 Scheduler stopped")
    
    async def cleanup_expired_links(self):
        """Clean up expired links"""
        try:
            from database.connection import get_database
            from database.queries.link_queries import LinkQueries
            
            db = await get_database()
            link_queries = LinkQueries(db)
            count = await link_queries.cleanup_expired_links()
            
            if count > 0:
                print(f"🧹 Cleaned up {count} expired links")
        except Exception as e:
            print(f"❌ Cleanup error: {e}")
    
    async def update_analytics(self):
        """Update analytics cache"""
        try:
            from services.analytics_service import analytics_service
            await analytics_service.update_global_stats()
            print("📊 Analytics updated")
        except Exception as e:
            print(f"❌ Analytics update error: {e}")

# Global scheduler instance
scheduler = BotScheduler()