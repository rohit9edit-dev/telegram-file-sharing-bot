from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.connection import get_database
from services.link_service import LinkService
from services.file_service import FileService
from utils.formatter import format_link, format_time_remaining, format_file_size
from core.bot_client import bot_client

def setup_handlers(app: Client):
    """Setup link management handlers"""
    
    @app.on_message(filters.command(["links"]) & filters.private)
    async def links_handler(client: Client, message: Message):
        """Handle /links command - show user's active links"""
        user_id = message.from_user.id
        
        db = await get_database()
        link_service = LinkService(db)
        file_service = FileService(db)
        
        # Get user's active links
        links = await link_service.get_user_links(user_id, active_only=True)
        
        if not links:
            await message.reply_text(
                "🔗 You don't have any active links.\n\n"
                "Upload a file to create a download link!"
            )
            return
        
        # Build response
        response = "🔗 Your Active Download Links:\n\n"
        bot_username = bot_client.get_username()
        
        for idx, link in enumerate(links[:20], 1):  # Limit to 20
            file = await file_service.get_file(link.file_id)
            if file:
                download_link = format_link(link.link_id, bot_username)
                time_remaining = format_time_remaining(link.expires_at) if link.expires_at else "Never"
                
                response += f"{idx}. {file.file_name}\n"
                response += f"   💾 {format_file_size(file.file_size)}\n"
                response += f"   🔗 {download_link}\n"
                response += f"   📄 Accesses: {link.access_count}"
                if link.max_access:
                    response += f"/{link.max_access}"
                response += f"\n   ⏰ Expires: {time_remaining}\n"
                response += f"   🆔 ID: `{link.link_id}`\n\n"
        
        response += "\nℹ️ Use /revoke <link_id> to revoke a link"
        
        await message.reply_text(response)
    
    @app.on_message(filters.command(["revoke"]) & filters.private)
    async def revoke_handler(client: Client, message: Message):
        """Handle /revoke command - revoke a download link"""
        if len(message.command) < 2:
            await message.reply_text(
                "ℹ️ Usage: /revoke <link_id>\n\n"
                "Get link IDs from /links command."
            )
            return
        
        link_id = message.command[1]
        user_id = message.from_user.id
        
        db = await get_database()
        link_service = LinkService(db)
        
        # Revoke link
        success = await link_service.revoke_link(link_id, user_id)
        
        if success:
            await message.reply_text(
                f"✅ Link revoked successfully!\n\n"
                f"🆔 Link ID: `{link_id}`\n\n"
                "This link can no longer be used to download the file."
            )
        else:
            await message.reply_text(
                "❌ Failed to revoke link. Make sure the link ID is correct "
                "and you own this link."
            )