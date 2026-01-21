#!/usr/bin/env python3
"""
Verification script to check bot setup
"""

import os
import sys

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("🔍 Checking .env file...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("ℹ️  Copy .env.example to .env and fill in your configuration")
        return False
    
    required_vars = [
        'BOT_TOKEN',
        'API_ID', 
        'API_HASH',
        'STORAGE_CHANNEL_ID',
        'MONGO_URL'
    ]
    
    missing = []
    with open('.env', 'r') as f:
        content = f.read()
        for var in required_vars:
            if f"{var}=" not in content or f"{var}=\n" in content:
                missing.append(var)
    
    if missing:
        print(f"⚠️  Missing required variables: {', '.join(missing)}")
        return False
    
    print("✅ .env file looks good")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("🔍 Checking dependencies...")
    
    required = [
        'pyrogram',
        'pymongo',
        'redis',
        'cryptography',
        'pydantic',
        'apscheduler'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("ℹ️  Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed")
    return True

def check_directory_structure():
    """Check if all required directories exist"""
    print("🔍 Checking directory structure...")
    
    required_dirs = [
        'core',
        'handlers',
        'services',
        'storage',
        'database',
        'database/models',
        'database/queries',
        'database/migrations',
        'utils',
        'cache',
        'plugins',
        'scripts'
    ]
    
    missing = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing.append(dir_path)
    
    if missing:
        print(f"❌ Missing directories: {', '.join(missing)}")
        return False
    
    print("✅ Directory structure is correct")
    return True

def check_mongodb():
    """Check MongoDB connection"""
    print("🔍 Checking MongoDB connection...")
    
    try:
        from pymongo import MongoClient
        from config import config
        
        client = MongoClient(config.MONGO_URL, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("ℹ️  Make sure MongoDB is running and MONGO_URL is correct")
        return False

def check_redis():
    """Check Redis connection (optional)"""
    print("🔍 Checking Redis connection...")
    
    try:
        import redis
        from config import config
        
        r = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            password=config.REDIS_PASSWORD,
            socket_connect_timeout=5
        )
        r.ping()
        print("✅ Redis connection successful")
        return True
    except Exception as e:
        print(f"⚠️  Redis connection failed: {e}")
        print("ℹ️  Redis is optional, bot will work without it")
        return True  # Don't fail on Redis

def main():
    """Main verification function"""
    print("🚀 Telegram File Sharing Bot - Setup Verification\n")
    
    checks = [
        check_directory_structure(),
        check_dependencies(),
        check_env_file(),
        check_mongodb(),
        check_redis()
    ]
    
    print("\n" + "="*50)
    
    if all(checks[:4]):  # Redis is optional
        print("✅ All critical checks passed!")
        print("\n🚀 You can now start the bot with: python bot.py")
        print("\nℹ️  Make sure to:")
        print("   1. Fill in all required values in .env")
        print("   2. Add the bot to your storage channel as admin")
        print("   3. Get your admin user ID from @userinfobot")
        return 0
    else:
        print("❌ Some checks failed!")
        print("\nℹ️  Please fix the issues above before starting the bot")
        return 1

if __name__ == '__main__':
    sys.exit(main())