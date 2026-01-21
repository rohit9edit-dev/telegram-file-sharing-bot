from pyrogram import Client, filters
from pyrogram.types import Message
from database.connection import get_database
from services.file_service import FileService
from services.link_service import LinkService
from storage.channel_manager import ChannelManager
from utils.formatter import format_file_size, format_link
from utils.constants import ALLOWED_FILE_TYPES
from config import config
from core.bot_client import bot_client
import os
import tempfile

def setup_handlers(app: Client):
    """Setup upload handlers"""
    
    @app.on_message(filters.document | filters.video | filters.audio | filters.photo)
    async def file_upload_handler(client: Client, message: Message):
        """Handle file uploads"""
        user_id = message.from_user.id
        
        # Get file info
        if message.document:
            file = message.document
            file_type = 'document'
            file_name = file.file_name
            file_size = file.file_size
            mime_type = file.mime_type
        elif message.video:
            file = message.video
            file_type = 'video'
            file_name = f"video_{file.file_unique_id}.mp4"
            file_size = file.file_size
            mime_type = file.mime_type
        elif message.audio:
            file = message.audio
            file_type = 'audio'
            file_name = file.file_name or f"audio_{file.file_unique_id}.mp3"
            file_size = file.file_size
            mime_type = file.mime_type
        elif message.photo:
            file = message.photo
            file_type = 'photo'
            file_name = f"photo_{message.id}.jpg"
            file_size = file.file_size
            mime_type = 'image/jpeg'
        else:
            return
        
        # Check file size
        max_size_mb = config.MAX_FILE_SIZE
        max_size_bytes = max_size_mb * 1024 * 1024
        
        if file_size > max_size_bytes:
            await message.reply_text(
                f"❌ File is too large! Maximum size: {max_size_mb}MB\n"
                f"Your file: {format_file_size(file_size)}"
            )
            return
        
        # Send processing message
        status_msg = await message.reply_text(
            f"📤 Uploading {file_name}...\n"
            f"💾 Size: {format_file_size(file_size)}"
        )
        
        try:
            db = await get_database()
            file_service = FileService(db)
            link_service = LinkService(db)
            channel_manager = ChannelManager(client)
            
            # Forward to storage channel
            forwarded = await client.forward_messages(
                chat_id=config.STORAGE_CHANNEL_ID,
                from_chat_id=message.chat.id,
                message_ids=message.id
            )
            
            if not forwarded:
                await status_msg.edit_text("❌ Failed to upload file.")
                return
            
            # Create file record
            file_record = await file_service.create_file_record(
                user_id=user_id,
                telegram_file_id=file.file_id,
                telegram_message_id=forwarded.id,
                file_name=file_name,
                file_size=file_size,
                file_type=file_type,
                mime_type=mime_type,
                is_encrypted=False
            )
            
            if not file_record:
                await status_msg.edit_text("❌ Failed to create file record.")
                return
            
            # Create download link
            link = await link_service.create_link(
                file_id=file_record.file_id,
                user_id=user_id,
                expiry_days=config.LINK_EXPIRY_DAYS
            )
            
            if not link:
                await status_msg.edit_text("❌ Failed to create download link.")
                return
            
            # Format download link
            bot_username = bot_client.get_username()
            download_link = format_link(link.link_id, bot_username)
            
            # Send success message
            await status_msg.edit_text(
                f"✅ File uploaded successfully!\n\n"
                f"📁 Name: {file_name}\n"
                f"💾 Size: {format_file_size(file_size)}\n"
                f"🆔 File ID: `{file_record.file_id}`\n\n"
                f"🔗 Download Link:\n{download_link}\n\n"
                f"⏰ Expires in {config.LINK_EXPIRY_DAYS} days"
            )
            
        except Exception as e:
            print(f"Upload error: {e}")
            await status_msg.edit_text(
                f"❌ Error uploading file: {str(e)}"
            )
    
    @app.on_message(filters.command(["upload"]) & filters.private)
    async def upload_command_handler(client: Client, message: Message):
        """Handle /upload command"""
        await message.reply_text(
            "📤 To upload a file, simply send it to me!\n\n"
            "Supported types:\n"
            "• Documents (PDF, DOCX, ZIP, etc.)\n"
            "• Videos\n"
            "• Audio files\n"
            "• Photos\n\n"
            f"⚠️ Maximum file size: {config.MAX_FILE_SIZE}MB"
        )