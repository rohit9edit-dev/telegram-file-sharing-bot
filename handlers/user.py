from pyrogram import Client, filters
from pyrogram.types import Message
from database.connection import get_database
from services.user_service import UserService
from services.file_service import FileService
from services.analytics_service import AnalyticsServiceFactory
from utils.formatter import format_file_size, format_datetime

def setup_handlers(app: Client):
    """Setup user-related handlers"""
    
    @app.on_message(filters.command(["myfiles"]) & filters.private)
    async def myfiles_handler(client: Client, message: Message):
        """Handle /myfiles command"""
        user_id = message.from_user.id
        
        db = await get_database()
        file_service = FileService(db)
        
        # Get user files
        files = await file_service.get_user_files(user_id, limit=20)
        
        if not files:
            await message.reply_text(
                "📁 You don't have any files yet.\n\n"
                "Send me a file to get started!"
            )
            return
        
        # Build response
        response = "📁 Your Files:\n\n"
        
        for idx, file in enumerate(files, 1):
            response += f"{idx}. {file.file_name}\n"
            response += f"   💾 {format_file_size(file.file_size)}\n"
            response += f"   📥 Downloads: {file.download_count}\n"
            response += f"   📅 {format_datetime(file.created_at)}\n"
            response += f"   🆔 `{file.file_id}`\n\n"
        
        response += "\nℹ️ Use /download <file_id> to download\n"
        response += "ℹ️ Use /search <query> to search files"
        
        await message.reply_text(response)
    
    @app.on_message(filters.command(["stats"]) & filters.private)
    async def stats_handler(client: Client, message: Message):
        """Handle /stats command"""
        user_id = message.from_user.id
        
        db = await get_database()
        analytics_service = AnalyticsServiceFactory.create(db)
        
        # Get user stats
        stats = await analytics_service.get_user_stats(user_id)
        
        if not stats:
            await message.reply_text("❌ Unable to fetch statistics.")
            return
        
        response = "📊 Your Statistics:\n\n"
        response += f"📁 Total Files: {stats.get('total_files', 0)}\n"
        response += f"💾 Storage Used: {format_file_size(stats.get('total_size', 0))}\n"
        response += f"🔗 Active Links: {stats.get('active_links', 0)}\n"
        response += f"📥 Total Downloads: {stats.get('total_downloads', 0)}\n"
        response += f"🎯 Tier: {stats.get('tier', 'free').title()}\n"
        
        if stats.get('member_since'):
            response += f"\n📅 Member Since: {format_datetime(stats['member_since'])}\n"
        
        await message.reply_text(response)

# ===============================
# Force Join Callback (Bottom)
# ===============================
from pyrogram import filters, Client
from core.middleware import force_join_required

@Client.on_callback_query(filters.regex("check_force_join"))
async def force_join_callback(client, callback_query):
    ok = await force_join_required(lambda c, m: True)(client, callback_query.message)
    if ok:
        await callback_query.message.edit_text("✅ Thanks! Ab bot use kar sakte ho.")
    else:
        await callback_query.answer("❌ Abhi bhi channel join nahi kiya", show_alert=True)
