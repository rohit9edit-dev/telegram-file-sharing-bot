# Quick Start Guide

Get your Telegram File Sharing Bot up and running in minutes!

## Prerequisites

- Python 3.8 or higher
- MongoDB (running locally or remote)
- Redis (optional, for caching)
- Telegram account

## Step-by-Step Setup

### 1. Install Dependencies

```bash
cd /app/telegram-bot
pip install -r requirements.txt
```

### 2. Get Telegram Credentials

#### Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Choose a name and username for your bot
4. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### API ID & API Hash
1. Visit [https://my.telegram.org](https://my.telegram.org)
2. Login with your phone number
3. Click on "API development tools"
4. Fill the form to create a new application
5. Copy your `api_id` (number) and `api_hash` (string)

### 3. Create Storage Channel

1. In Telegram, create a new channel (not a group)
2. Make it **Private**
3. Add your bot as an administrator
4. Get the channel ID:
   - Forward any message from the channel to [@getidsbot](https://t.me/getidsbot)
   - Copy the channel ID (looks like: `-1001234567890`)

### 4. Get Your User ID

1. Message [@userinfobot](https://t.me/userinfobot) on Telegram
2. Copy your user ID (number)

### 5. Configure Environment

Edit the `.env` file:

```bash
nano .env
```

Fill in your credentials:

```env
# Telegram Bot Configuration
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
API_ID=12345678
API_HASH=abcdef1234567890abcdef1234567890

# Storage Channel
STORAGE_CHANNEL_ID=-1001234567890

# Admin Configuration (your user ID)
ADMIN_IDS=123456789

# Database (default is fine for local MongoDB)
MONGO_URL=mongodb://localhost:27017
DB_NAME=telegram_file_bot

# Redis (default is fine for local Redis)
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 6. Verify Setup

Run the verification script:

```bash
python scripts/verify_setup.py
```

This will check:
- Directory structure
- Dependencies
- Environment configuration
- Database connection
- Redis connection (optional)

### 7. Run Database Migrations

```bash
python scripts/migrate.py
```

### 8. Start the Bot

```bash
python bot.py
```

You should see:

```
🚀 Starting Telegram File Sharing Bot...

💾 Connecting to MongoDB...
✅ Database connected successfully
🐝 Connecting to Redis...
✅ Redis connected successfully
🤖 Initializing bot client...
✅ Bot started: @your_bot_username
🔄 Loading handlers...
✅ All handlers loaded
⏰ Starting scheduler...
✅ Scheduler started
✅ Storage channel verified

✅ Bot started successfully!
🤖 Bot username: @your_bot_username
📡 Listening for messages...
```

### 9. Test the Bot

1. Open Telegram and search for your bot
2. Send `/start`
3. You should receive a welcome message
4. Try uploading a file

## Common Commands

### User Commands
- `/start` - Start the bot
- `/help` - Show help
- `/myfiles` - View your files
- `/links` - View download links
- `/stats` - Your statistics

### Admin Commands
- `/admin` - Admin panel
- `/users` - List users
- `/stats_all` - Global stats

## Troubleshooting

### Bot doesn't respond
- Check if bot token is correct
- Verify bot is running without errors
- Check internet connection

### Can't upload files
- Verify storage channel ID is correct
- Make sure bot is admin in the channel
- Check bot has posting permissions

### Database errors
- Ensure MongoDB is running: `sudo systemctl status mongod`
- Test connection: `mongosh`

### Redis not working
- Redis is optional, bot works without it
- Start Redis: `sudo systemctl start redis`

## Next Steps

- Customize bot messages in `utils/constants.py`
- Add more admin users to `ADMIN_IDS` in `.env`
- Set up automatic backups: `crontab -e`
- Configure file size limits in `.env`
- Enable features like encryption and self-destruct

## Production Deployment

For production:

1. Use strong encryption keys
2. Set up proper logging
3. Configure rate limiting
4. Use environment secrets management
5. Set up monitoring
6. Regular database backups
7. Use process manager (PM2, systemd)

Example systemd service:

```ini
[Unit]
Description=Telegram File Sharing Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/app/telegram-bot
ExecStart=/usr/bin/python3 /app/telegram-bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Support

- Check README.md for detailed documentation
- Review error logs in console output
- Verify all configuration values are correct

## License

MIT License - Free to use and modify

---

**Happy File Sharing! 🚀**
