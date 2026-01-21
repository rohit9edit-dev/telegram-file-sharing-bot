from pyrogram import Client, filters
from pyrogram.types import Message
from database.connection import get_database
from services.file_service import FileService
from services.link_service import LinkService
from storage.channel_manager import ChannelManager
from utils.formatter import format_file_size

def setup_handlers(app: Client):
    """Setup download handlers"""
    
    @app.on_message(filters.command(["download"]) & filters.private)
    async def download_handler(client: Client, message: Message):
        """Handle /download command"""
        if len(message.command) < 2:
            await message.reply_text(
                "ℹ️ Usage: /download <file_id>\n\n"
                "Get your file ID from /myfiles command."
            )
            return
        
        file_id = message.command[1]
        user_id = message.from_user.id
        
        db = await get_database()
        file_service = FileService(db)
        
        # Get file
        file = await file_service.get_file(file_id)
        if not file:
            await message.reply_text("❌ File not found.")
            return
        
        # Check ownership
        if file.user_id != user_id:
            await message.reply_text("❌ You don't have access to this file.")
            return
        
        # Send file
        try:
            channel_manager = ChannelManager(client)
            await message.reply_text("📥 Preparing your file...")
            
            await channel_manager.copy_file(
                message_id=file.telegram_message_id,
                to_chat_id=message.chat.id,
                caption=f"📁 {file.file_name}\n💾 {format_file_size(file.file_size)}"
            )
            
            await message.reply_text("✅ File sent successfully!")
            
        except Exception as e:
            print(f"Download error: {e}")
            await message.reply_text("❌ Error downloading file.")