# Bot Messages
WELCOME_MESSAGE = """👋 Welcome to File Sharing Bot!

I can help you:
📤 Upload and store files securely
📥 Generate shareable download links
🔐 Encrypt files for privacy
⏰ Create self-destructing files
📊 Track file analytics

Use /help to see all commands."""

HELP_MESSAGE = """📖 Available Commands:

👤 User Commands:
/start - Start the bot
/help - Show this help message
/upload - Upload a file
/myfiles - View your uploaded files
/stats - View your usage statistics

🔗 Link Commands:
/links - View your active links
/revoke <link_id> - Revoke a download link

🔍 Search:
/search <query> - Search your files

👨‍💼 Admin Commands:
/admin - Admin panel
/users - List all users
/broadcast <message> - Broadcast to all users
/stats_all - Global statistics

Just send me a file to upload it!"""

ADMIN_PANEL = """👨‍💼 Admin Panel

Available admin commands:
/users - List all users
/ban <user_id> - Ban a user
/unban <user_id> - Unban a user
/broadcast <message> - Send message to all users
/stats_all - View global statistics
/cleanup - Run cleanup tasks"""

# File Types
ALLOWED_FILE_TYPES = [
    'document', 'video', 'audio', 'photo', 'voice', 'video_note'
]

# Link Status
LINK_STATUS_ACTIVE = 'active'
LINK_STATUS_EXPIRED = 'expired'
LINK_STATUS_REVOKED = 'revoked'
LINK_STATUS_USED = 'used'

# User Roles
ROLE_USER = 'user'
ROLE_ADMIN = 'admin'
ROLE_BANNED = 'banned'

# Cache TTL (seconds)
CACHE_TTL_USER = 3600  # 1 hour
CACHE_TTL_FILE = 1800  # 30 minutes
CACHE_TTL_LINK = 3600  # 1 hour

# Rate Limiting
RATE_LIMIT_MESSAGES = 20  # messages per minute
RATE_LIMIT_UPLOADS = 10   # uploads per hour

# Subscription Tiers (for future use)
TIER_FREE = 'free'
TIER_BASIC = 'basic'
TIER_PRO = 'pro'
TIER_ENTERPRISE = 'enterprise'

TIER_LIMITS = {
    TIER_FREE: {
        'max_file_size': 100,  # MB
        'max_files': 50,
        'link_expiry': 7,  # days
    },
    TIER_BASIC: {
        'max_file_size': 500,
        'max_files': 200,
        'link_expiry': 30,
    },
    TIER_PRO: {
        'max_file_size': 2000,
        'max_files': 1000,
        'link_expiry': 90,
    },
    TIER_ENTERPRISE: {
        'max_file_size': 5000,
        'max_files': -1,  # unlimited
        'link_expiry': 365,
    }
}