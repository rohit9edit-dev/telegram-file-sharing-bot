from pyrogram import Client, filters
from pyrogram.types import Message
from database.connection import get_database
from services.file_service import FileService
from utils.formatter import format_file_size, format_datetime

def setup_handlers(app: Client):
    """Setup search handlers"""
    
    @app.on_message(filters.command(["search"]) & filters.private)
    async def search_handler(client: Client, message: Message):
        """Handle /search command"""
        if len(message.command) < 2:
            await message.reply_text(
                "ℹ️ Usage: /search <query>\n\n"
                "Example: /search report.pdf"
            )
            return
        
        query = ' '.join(message.command[1:])
        user_id = message.from_user.id
        
        db = await get_database()
        file_service = FileService(db)
        
        # Search files
        files = await file_service.search_files(user_id, query)
        
        if not files:
            await message.reply_text(
                f"🔍 No files found matching: {query}"
            )
            return
        
        # Build response
        response = f"🔍 Search Results for: {query}\n\n"
        
        for idx, file in enumerate(files[:15], 1):  # Limit to 15
            response += f"{idx}. {file.file_name}\n"
            response += f"   💾 {format_file_size(file.file_size)}\n"
            response += f"   📅 {format_datetime(file.created_at)}\n"
            response += f"   🆔 `{file.file_id}`\n\n"
        
        response += "\nℹ️ Use /download <file_id> to download a file"
        
        await message.reply_text(response)