from pyrogram import Client, filters
from pyrogram.types import Message
from utils.constants import WELCOME_MESSAGE, HELP_MESSAGE
from database.connection import get_database
from services.user_service import UserService
from services.link_service import LinkService
from services.file_service import FileService

def setup_handlers(app: Client):
    """Setup start command handlers"""
    
    @app.on_message(filters.command(["start"]) & filters.private)
    async def start_handler(client: Client, message: Message):
        """Handle /start command"""
        user = message.from_user
        db = await get_database()
        user_service = UserService(db)
        
        # Get or create user
        await user_service.get_or_create_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # Check if it's a download link
        if len(message.command) > 1:
            param = message.command[1]
            if param.startswith('dl_'):
                link_id = param[3:]
                await handle_download_link(client, message, link_id)
                return
        
        # Send welcome message
        await message.reply_text(WELCOME_MESSAGE)
    
    @app.on_message(filters.command(["help"]) & filters.private)
    async def help_handler(client: Client, message: Message):
        """Handle /help command"""
        await message.reply_text(HELP_MESSAGE)

async def handle_download_link(client: Client, message: Message, link_id: str):
    """Handle download link from start parameter"""
    db = await get_database()
    link_service = LinkService(db)
    file_service = FileService(db)
    
    # Get link
    link = await link_service.get_link(link_id)
    if not link:
        await message.reply_text("❌ Invalid download link.")
        return
    
    # Validate and access link
    success, error = await link_service.access_link(link_id, message.from_user.id)
    if not success:
        await message.reply_text(error)
        return
    
    # Get file
    file = await file_service.get_file(link.file_id)
    if not file:
        await message.reply_text("❌ File not found.")
        return
    
    # Send file
    try:
        from storage.channel_manager import ChannelManager
        channel_manager = ChannelManager(client)
        
        await message.reply_text("📥 Preparing your file...")
        
        # Forward file from channel
        await channel_manager.copy_file(
            message_id=file.telegram_message_id,
            to_chat_id=message.chat.id,
            caption=f"📁 {file.file_name}\n\n💾 Size: {format_file_size(file.file_size)}"
        )
        
        # Increment download count
        await file_service.increment_download(file.file_id)
        
        await message.reply_text("✅ File sent successfully!")
        
    except Exception as e:
        print(f"Error sending file: {e}")
        await message.reply_text("❌ Error sending file. Please try again later.")

def format_file_size(size_bytes: int) -> str:
    """Format file size"""
    from utils.formatter import format_file_size
    return format_file_size(size_bytes)