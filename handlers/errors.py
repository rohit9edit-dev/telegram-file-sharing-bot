from pyrogram import Client
from pyrogram.errors import RPCError
import traceback

def setup_handlers(app: Client):
    """Setup error handlers"""
    
    @app.on_error()
    async def error_handler(client: Client, error: Exception):
        """Global error handler"""
        print(f"❌ Error occurred: {error}")
        print(traceback.format_exc())
        
        # Log to database (optional)
        # await log_error_to_db(error)
        
        return True  # Continue handling other updates