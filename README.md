# Telegram File Sharing Bot

A production-ready Telegram bot for secure file sharing with advanced features like encryption, self-destructing links, and analytics.

## Features

### Core Features
- 📤 **File Upload & Storage**: Upload files to private Telegram channel
- 🔗 **Shareable Links**: Generate secure download links
- 📥 **Easy Download**: Download files via unique links
- 🔍 **Search**: Search through your uploaded files
- 📊 **Analytics**: Track downloads and usage statistics

### Security Features
- 🔐 **Encryption**: Optional file encryption for sensitive data
- ⏰ **Self-Destruct**: Create time-limited download links
- 🔒 **Access Control**: JWT-style user authentication
- 📝 **Audit Logs**: Track all file operations

### Admin Features
- 👨‍💼 **User Management**: Ban/unban users
- 📢 **Broadcast**: Send messages to all users
- 📊 **Global Stats**: View platform statistics
- 🔧 **Cleanup Tools**: Automated maintenance tasks

## Requirements

- Python 3.8+
- MongoDB
- Redis (optional, for caching)
- Telegram Bot Token
- Private Telegram Channel for storage

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd telegram-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your configuration:

```bash
cp .env.example .env
```

Required variables:

```env
# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_from_botfather
API_ID=your_api_id_from_my.telegram.org
API_HASH=your_api_hash_from_my.telegram.org

# Storage Channel
STORAGE_CHANNEL_ID=-1001234567890

# Admin User IDs (comma-separated)
ADMIN_IDS=123456789,987654321

# Database
MONGO_URL=mongodb://localhost:27017
DB_NAME=telegram_file_bot

# Redis (optional)
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 4. Get Telegram credentials

**Bot Token:**
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy the bot token

**API ID & Hash:**
1. Visit [my.telegram.org](https://my.telegram.org)
2. Login with your phone number
3. Go to "API development tools"
4. Create a new application
5. Copy API ID and API Hash

**Storage Channel:**
1. Create a private Telegram channel
2. Add your bot as an admin
3. Get the channel ID using [@getidsbot](https://t.me/getidsbot)

**Admin User ID:**
1. Message [@userinfobot](https://t.me/userinfobot)
2. Copy your user ID

### 5. Run migrations

```bash
python scripts/migrate.py
```

### 6. Start the bot

```bash
python bot.py
```

## Usage

### User Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/upload` - Instructions for uploading files
- `/myfiles` - View your uploaded files
- `/links` - View your active download links
- `/revoke <link_id>` - Revoke a download link
- `/search <query>` - Search your files
- `/download <file_id>` - Download a specific file
- `/stats` - View your usage statistics

### Admin Commands

- `/admin` - Show admin panel
- `/users` - List all users
- `/ban <user_id>` - Ban a user
- `/unban <user_id>` - Unban a user
- `/broadcast <message>` - Broadcast to all users
- `/stats_all` - View global statistics

### File Upload

Simply send any file to the bot:
- Documents (PDF, DOCX, ZIP, etc.)
- Videos
- Audio files
- Photos

The bot will:
1. Upload to storage channel
2. Create a database record
3. Generate a shareable download link
4. Return the link with expiry information

### Download via Link

Users can access files via links like:
```
https://t.me/your_bot?start=dl_<link_id>
```

## Project Structure

```
telegram-bot/
├── bot.py                 # Main entry point
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── README.md              # This file
├── .env.example           # Environment template
├── core/                  # Core bot components
│   ├── client.py
│   ├── dispatcher.py
│   ├── middleware.py
│   └── scheduler.py
├── handlers/              # Message handlers
│   ├── start.py
│   ├── upload.py
│   ├── download.py
│   ├── links.py
│   ├── search.py
│   ├── user.py
│   ├── admin.py
│   └── errors.py
├── services/              # Business logic
│   ├── file_service.py
│   ├── link_service.py
│   ├── user_service.py
│   ├── security_service.py
│   ├── analytics_service.py
│   ├── subscription_service.py
│   └── payment_service.py
├── storage/               # File storage management
│   ├── channel_manager.py
│   ├── mirror_manager.py
│   └── cache_manager.py
├── database/              # Database layer
│   ├── connection.py
│   ├── models/            # Pydantic models
│   ├── queries/           # Database queries
│   └── migrations/        # Migration scripts
├── utils/                 # Utilities
│   ├── hash.py
│   ├── encryption.py
│   ├── validators.py
│   ├── formatter.py
│   └── constants.py
├── cache/                 # Redis cache
│   ├── redis_client.py
│   └── keys.py
├── plugins/               # Optional features
│   ├── vault.py
│   ├── self_destruct.py
│   ├── watermark.py
│   └── experimental.py
└── scripts/               # Utility scripts
    ├── cleanup.py
    ├── migrate.py
    └── backup.py
```

## Maintenance Scripts

### Run cleanup

Clean up expired links and old logs:

```bash
python scripts/cleanup.py
```

### Database backup

Backup database to JSON files:

```bash
python scripts/backup.py
```

Restore from backup:

```bash
python scripts/backup.py restore /tmp/backups/backup_20240101_120000
```

## Configuration Options

### File Settings

- `MAX_FILE_SIZE`: Maximum file size in MB (default: 2000)
- `LINK_EXPIRY_DAYS`: Default link expiry in days (default: 7)

### Feature Toggles

- `ENABLE_ANALYTICS`: Track analytics (default: true)
- `ENABLE_ENCRYPTION`: Enable file encryption (default: true)
- `ENABLE_SELF_DESTRUCT`: Enable self-destruct feature (default: true)
- `ENABLE_WATERMARK`: Enable watermark feature (default: false)
- `ENABLE_PAYMENTS`: Enable payment integration (default: false)

## Architecture

### Database Models

- **User**: User accounts and statistics
- **File**: File metadata and references
- **Link**: Download links with access control
- **AccessLog**: Download access logs
- **AuditLog**: Action audit trail
- **Subscription**: User subscriptions (future)
- **Referral**: Referral program (future)

### Services

- **FileService**: File management operations
- **LinkService**: Link generation and validation
- **UserService**: User management
- **SecurityService**: Encryption and security
- **AnalyticsService**: Statistics and analytics
- **SubscriptionService**: Subscription management (placeholder)
- **PaymentService**: Payment processing (placeholder)

### Storage

- **ChannelManager**: Manage Telegram channel storage
- **MirrorManager**: File mirroring across channels
- **CacheManager**: Redis caching layer

## Development

### Adding new features

1. Create handler in `handlers/`
2. Add service logic in `services/`
3. Update models if needed in `database/models/`
4. Add queries in `database/queries/`
5. Register handler in dispatcher

### Testing

1. Set up test environment with test bot and channel
2. Configure `.env` with test credentials
3. Run the bot and test commands
4. Check logs for errors

## Troubleshooting

### Bot not responding

- Check if bot token is correct
- Verify bot is running without errors
- Check network connectivity

### Can't upload files

- Verify storage channel ID is correct
- Check if bot is admin in the channel
- Ensure bot has message posting permissions

### Database errors

- Verify MongoDB is running
- Check connection string in `.env`
- Run migrations: `python scripts/migrate.py`

### Cache not working

- Redis is optional, bot will work without it
- Check Redis connection settings
- Verify Redis is running

## Security Considerations

- Never share your `.env` file
- Keep bot token secret
- Use strong encryption keys in production
- Regularly backup your database
- Monitor audit logs for suspicious activity
- Implement rate limiting for production

## Future Enhancements

- [ ] Payment integration (Stripe, PayPal)
- [ ] Subscription tiers with different limits
- [ ] File compression before upload
- [ ] Thumbnail generation
- [ ] QR code generation for links
- [ ] Batch file operations
- [ ] File sharing between users
- [ ] OAuth integration
- [ ] Web dashboard
- [ ] Mobile app

## License

MIT License - Feel free to use and modify

## Support

For issues and questions:
- Open an issue on GitHub
- Check documentation
- Review error logs

## Credits

Built with:
- [Pyrogram](https://pyrogram.org/) - Telegram MTProto API framework
- [MongoDB](https://www.mongodb.com/) - Database
- [Redis](https://redis.io/) - Cache
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation

---

**Made with ❤️ for the Telegram community**