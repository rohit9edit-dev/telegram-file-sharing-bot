import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Telegram Bot
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', '')
    API_ID: int = int(os.getenv('API_ID', '0'))
    API_HASH: str = os.getenv('API_HASH', '')
    
    # Storage
    STORAGE_CHANNEL_ID: int = int(os.getenv('STORAGE_CHANNEL_ID', '0'))

    # Force Channel Join
FORCE_JOIN = os.getenv("FORCE_JOIN", "true").lower() == "true"

FORCE_JOIN_CHANNELS = [
    int(x.strip())
    for x in os.getenv("FORCE_JOIN_CHANNELS", "").split(",")
    if x.strip()
]

    # Admin
    ADMIN_IDS: List[int] = [
        int(id_.strip()) 
        for id_ in os.getenv('ADMIN_IDS', '').split(',') 
        if id_.strip()
    ]
    
    # Database
    MONGO_URL: str = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    DB_NAME: str = os.getenv('DB_NAME', 'telegram_file_bot')
    
    # Redis
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_PASSWORD: Optional[str] = os.getenv('REDIS_PASSWORD') or None
    REDIS_DB: int = int(os.getenv('REDIS_DB', '0'))
    
    # Security
    ENCRYPTION_KEY: str = os.getenv('ENCRYPTION_KEY', 'default_key_please_change_in_prod')
    JWT_SECRET: str = os.getenv('JWT_SECRET', 'default_jwt_secret_change_me')
    
    # Bot Settings
    MAX_FILE_SIZE: int = int(os.getenv('MAX_FILE_SIZE', '2000'))  # MB
    LINK_EXPIRY_DAYS: int = int(os.getenv('LINK_EXPIRY_DAYS', '7'))
    ENABLE_ANALYTICS: bool = os.getenv('ENABLE_ANALYTICS', 'true').lower() == 'true'
    ENABLE_ENCRYPTION: bool = os.getenv('ENABLE_ENCRYPTION', 'true').lower() == 'true'
    
    # Features
    ENABLE_SELF_DESTRUCT: bool = os.getenv('ENABLE_SELF_DESTRUCT', 'true').lower() == 'true'
    ENABLE_WATERMARK: bool = os.getenv('ENABLE_WATERMARK', 'false').lower() == 'true'
    ENABLE_PAYMENTS: bool = os.getenv('ENABLE_PAYMENTS', 'false').lower() == 'true'
    
    @classmethod
    def validate(cls) -> bool:
        """Validate critical configuration"""
        if not cls.BOT_TOKEN:
            print("⚠️  BOT_TOKEN is not set!")
            return False
        if not cls.STORAGE_CHANNEL_ID:
            print("⚠️  STORAGE_CHANNEL_ID is not set!")
            return False
        return True

config = Config()
