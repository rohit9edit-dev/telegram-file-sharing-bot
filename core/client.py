from pyrogram import Client
from config import config
from typing import Optional

class BotClient:
    """Pyrogram bot client wrapper"""
    
    def __init__(self):
        self.app: Optional[Client] = None
        self.bot_username: Optional[str] = None
    
    def create_client(self) -> Client:
        """Create Pyrogram client"""
        self.app = Client(
            name="file_sharing_bot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            workdir="/tmp"
        )
        return self.app
    
    async def start(self):
        """Start the bot"""
        if not self.app:
            self.create_client()
        
        await self.app.start()
        me = await self.app.get_me()
        self.bot_username = me.username
        print(f"✅ Bot started: @{self.bot_username}")
        return self.app
    
    async def stop(self):
        """Stop the bot"""
        if self.app:
            await self.app.stop()
            print("🛑 Bot stopped")
    
    def get_app(self) -> Optional[Client]:
        """Get Pyrogram client instance"""
        return self.app
    
    def get_username(self) -> Optional[str]:
        """Get bot username"""
        return self.bot_username

# Global bot client instance
bot_client = BotClient()