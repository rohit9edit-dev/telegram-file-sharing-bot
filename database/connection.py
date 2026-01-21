from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from config import config
import asyncio
from typing import Optional

class DatabaseConnection:
    """MongoDB connection manager"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self.sync_client: Optional[MongoClient] = None
        
    async def connect(self):
        """Establish async database connection"""
        try:
            self.client = AsyncIOMotorClient(config.MONGO_URL)
            self.db = self.client[config.DB_NAME]
            # Test connection
            await self.client.admin.command('ping')
            print("✅ Database connected successfully")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def connect_sync(self):
        """Establish sync database connection for migrations"""
        try:
            self.sync_client = MongoClient(config.MONGO_URL)
            db = self.sync_client[config.DB_NAME]
            # Test connection
            self.sync_client.admin.command('ping')
            print("✅ Sync database connected")
            return db
        except Exception as e:
            print(f"❌ Sync database connection failed: {e}")
            return None
    
    async def disconnect(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("🔒 Database disconnected")
    
    async def create_indexes(self):
        """Create database indexes for performance"""
        try:
            # User indexes
            await self.db.users.create_index('user_id', unique=True)
            await self.db.users.create_index('role')
            await self.db.users.create_index('created_at')
            
            # File indexes
            await self.db.files.create_index('file_id', unique=True)
            await self.db.files.create_index('user_id')
            await self.db.files.create_index('created_at')
            await self.db.files.create_index('is_deleted')
            
            # Link indexes
            await self.db.links.create_index('link_id', unique=True)
            await self.db.links.create_index('file_id')
            await self.db.links.create_index('user_id')
            await self.db.links.create_index('status')
            await self.db.links.create_index('expires_at')
            
            # Access log indexes
            await self.db.access_logs.create_index('link_id')
            await self.db.access_logs.create_index('accessed_at')
            
            # Audit log indexes
            await self.db.audit_logs.create_index('user_id')
            await self.db.audit_logs.create_index('action')
            await self.db.audit_logs.create_index('timestamp')
            
            print("✅ Database indexes created")
        except Exception as e:
            print(f"⚠️  Error creating indexes: {e}")

# Global database instance
db_connection = DatabaseConnection()
db = None

async def get_database():
    """Get database instance"""
    global db
    if db is None:
        await db_connection.connect()
        db = db_connection.db
        await db_connection.create_indexes()
    return db