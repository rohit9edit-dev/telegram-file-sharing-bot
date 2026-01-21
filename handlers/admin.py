from pyrogram import Client, filters
from pyrogram.types import Message
from database.connection import get_database
from services.user_service import UserService
from services.analytics_service import AnalyticsServiceFactory
from core.middleware import admin_only
from utils.constants import ADMIN_PANEL
from utils.formatter import format_stats, format_file_size

def setup_handlers(app: Client):
    """Setup admin handlers"""
    
    @app.on_message(filters.command(["admin"]) & filters.private)
    @admin_only
    async def admin_panel_handler(client: Client, message: Message):
        """Handle /admin command"""
        await message.reply_text(ADMIN_PANEL)
    
    @app.on_message(filters.command(["users"]) & filters.private)
    @admin_only
    async def users_handler(client: Client, message: Message):
        """Handle /users command - list all users"""
        db = await get_database()
        user_service = UserService(db)
        
        users = await user_service.get_all_users(limit=50)
        
        if not users:
            await message.reply_text("👥 No users found.")
            return
        
        response = f"👥 Total Users: {len(users)}\n\n"
        
        for idx, user in enumerate(users[:20], 1):  # Limit to 20
            response += f"{idx}. "
            if user.username:
                response += f"@{user.username}"
            else:
                response += user.first_name or "Unknown"
            response += f" (ID: {user.user_id})\n"
            response += f"   📊 Files: {user.total_files} | "
            response += f"Storage: {format_file_size(user.total_size)}\n"
            response += f"   🎯 Role: {user.role}"
            if user.is_banned:
                response += " ❌ BANNED"
            response += "\n\n"
        
        await message.reply_text(response)
    
    @app.on_message(filters.command(["ban"]) & filters.private)
    @admin_only
    async def ban_handler(client: Client, message: Message):
        """Handle /ban command"""
        if len(message.command) < 2:
            await message.reply_text(
                "ℹ️ Usage: /ban <user_id>\n\n"
                "Get user IDs from /users command."
            )
            return
        
        try:
            target_user_id = int(message.command[1])
        except ValueError:
            await message.reply_text("❌ Invalid user ID.")
            return
        
        db = await get_database()
        user_service = UserService(db)
        
        success = await user_service.ban_user(target_user_id)
        
        if success:
            await message.reply_text(
                f"✅ User {target_user_id} has been banned."
            )
        else:
            await message.reply_text("❌ Failed to ban user.")
    
    @app.on_message(filters.command(["unban"]) & filters.private)
    @admin_only
    async def unban_handler(client: Client, message: Message):
        """Handle /unban command"""
        if len(message.command) < 2:
            await message.reply_text(
                "ℹ️ Usage: /unban <user_id>\n\n"
                "Get user IDs from /users command."
            )
            return
        
        try:
            target_user_id = int(message.command[1])
        except ValueError:
            await message.reply_text("❌ Invalid user ID.")
            return
        
        db = await get_database()
        user_service = UserService(db)
        
        success = await user_service.unban_user(target_user_id)
        
        if success:
            await message.reply_text(
                f"✅ User {target_user_id} has been unbanned."
            )
        else:
            await message.reply_text("❌ Failed to unban user.")
    
    @app.on_message(filters.command(["broadcast"]) & filters.private)
    @admin_only
    async def broadcast_handler(client: Client, message: Message):
        """Handle /broadcast command"""
        if len(message.command) < 2:
            await message.reply_text(
                "ℹ️ Usage: /broadcast <message>\n\n"
                "Send a message to all users."
            )
            return
        
        broadcast_text = ' '.join(message.command[1:])
        
        db = await get_database()
        user_service = UserService(db)
        
        users = await user_service.get_all_users(limit=10000)
        
        status_msg = await message.reply_text(
            f"📤 Broadcasting to {len(users)} users..."
        )
        
        success_count = 0
        fail_count = 0
        
        for user in users:
            try:
                await client.send_message(
                    chat_id=user.user_id,
                    text=f"📢 Announcement:\n\n{broadcast_text}"
                )
                success_count += 1
            except Exception as e:
                fail_count += 1
                print(f"Broadcast failed for {user.user_id}: {e}")
        
        await status_msg.edit_text(
            f"✅ Broadcast complete!\n\n"
            f"✅ Sent: {success_count}\n"
            f"❌ Failed: {fail_count}"
        )
    
    @app.on_message(filters.command(["stats_all"]) & filters.private)
    @admin_only
    async def stats_all_handler(client: Client, message: Message):
        """Handle /stats_all command - global statistics"""
        db = await get_database()
        analytics_service = AnalyticsServiceFactory.create(db)
        
        stats = await analytics_service.get_global_stats()
        
        if not stats:
            await message.reply_text("❌ Unable to fetch statistics.")
            return
        
        await message.reply_text(format_stats(stats))