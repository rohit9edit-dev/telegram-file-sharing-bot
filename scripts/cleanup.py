#!/usr/bin/env python3
"""Cleanup script for expired links and old files"""
import asyncio
import sys
sys.path.insert(0, '/app/telegram-bot')

from database.connection import DatabaseConnection
from database.queries.link_queries import LinkQueries
from datetime import datetime, timedelta
from config import config

async def cleanup_expired_links():
    """Clean up expired links"""
    print("🧹 Starting link cleanup...")
    
    db_conn = DatabaseConnection()
    await db_conn.connect()
    db = db_conn.db
    
    link_queries = LinkQueries(db)
    count = await link_queries.cleanup_expired_links()
    
    print(f"✅ Cleaned up {count} expired links")
    
    await db_conn.disconnect()

async def cleanup_old_access_logs(days: int = 90):
    """Remove old access logs"""
    print(f"🧹 Cleaning up access logs older than {days} days...")
    
    db_conn = DatabaseConnection()
    await db_conn.connect()
    db = db_conn.db
    
    cutoff = datetime.utcnow() - timedelta(days=days)
    result = await db.access_logs.delete_many({
        'accessed_at': {'$lt': cutoff}
    })
    
    print(f"✅ Removed {result.deleted_count} old access logs")
    
    await db_conn.disconnect()

async def cleanup_deleted_files():
    """Clean up soft-deleted files"""
    print("🧹 Cleaning up deleted files...")
    
    db_conn = DatabaseConnection()
    await db_conn.connect()
    db = db_conn.db
    
    # Find files deleted more than 30 days ago
    cutoff = datetime.utcnow() - timedelta(days=30)
    
    result = await db.files.delete_many({
        'is_deleted': True,
        'updated_at': {'$lt': cutoff}
    })
    
    print(f"✅ Removed {result.deleted_count} deleted files")
    
    await db_conn.disconnect()

async def main():
    """Main cleanup function"""
    print("🧹 Starting cleanup tasks...\n")
    
    await cleanup_expired_links()
    await cleanup_old_access_logs()
    await cleanup_deleted_files()
    
    print("\n✅ Cleanup completed!")

if __name__ == '__main__':
    asyncio.run(main())