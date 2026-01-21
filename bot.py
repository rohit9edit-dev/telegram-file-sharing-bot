#!/usr/bin/env python3
"""
Telegram File Sharing Bot
A production-ready bot for secure file sharing with MongoDB and Redis
"""

import asyncio
import signal
import sys
from pyrogram import idle

from config import config
from core.client import bot_client
from core.dispatcher import Dispatcher
from core.scheduler import scheduler
from database.connection import get_database
from cache.redis_client import redis_client

class FileShareBot:
    """Main bot application"""
    
    def __init__(self):
        self.app = None
        self.dispatcher = None
        self.running = False
    
    async def startup(self):
        """Initialize and start the bot"""
        print("🚀 Starting Telegram File Sharing Bot...\n")
        
        # Validate configuration
        if not config.validate():
            print("❌ Configuration validation failed!")
            print("ℹ️  Please check your .env file and ensure:")
            print("   - BOT_TOKEN is set")
            print("   - STORAGE_CHANNEL_ID is set")
            print("   - API_ID and API_HASH are configured")
            return False
        
        try:
            # Connect to database
            print("💾 Connecting to MongoDB...")
            db = await get_database()
            if not db:
                print("❌ Failed to connect to database")
                return False
            
            # Connect to Redis (optional)
            print("🐝 Connecting to Redis...")
            await redis_client.connect()
            
            # Create and start Pyrogram client
            print("🤖 Initializing bot client...")
            self.app = await bot_client.start()
            
            # Setup dispatcher and load handlers
            print("🔄 Loading handlers...")
            self.dispatcher = Dispatcher(self.app)
            self.dispatcher.load_all_handlers()
            self.dispatcher.load_plugins()
            
            # Start scheduler
            print("⏰ Starting scheduler...")
            scheduler.start()
            
            # Verify storage channel access
            from storage.channel_manager import ChannelManager
            channel_manager = ChannelManager(self.app)
            if await channel_manager.verify_channel_access():
                print("✅ Storage channel verified")
            else:
                print("⚠️  Storage channel not accessible!")
                print("ℹ️  Make sure the bot is added to the channel as admin")
            
            self.running = True
            print("\n✅ Bot started successfully!")
            print(f"🤖 Bot username: @{bot_client.get_username()}")
            print("📡 Listening for messages...\n")
            
            return True
            
        except Exception as e:
            print(f"❌ Startup error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def shutdown(self):
        """Gracefully shutdown the bot"""
        if not self.running:
            return
        
        print("\n\n🛑 Shutting down bot...")
        
        # Stop scheduler
        scheduler.stop()
        
        # Disconnect from Redis
        await redis_client.disconnect()
        
        # Stop Pyrogram client
        await bot_client.stop()
        
        print("✅ Bot stopped successfully")
        self.running = False
    
    async def run(self):
        """Run the bot"""
        # Start the bot
        if not await self.startup():
            return
        
        # Keep the bot running
        try:
            await idle()
        except KeyboardInterrupt:
            print("\n⏹️  Interrupted by user")
        finally:
            await self.shutdown()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\n⏹️  Received shutdown signal")
    sys.exit(0)

async def main():
    """Main entry point"""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run bot
    bot = FileShareBot()
    await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")