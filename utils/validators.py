import re
from typing import Optional, Tuple
from datetime import datetime, timedelta

def validate_file_size(size_bytes: int, max_mb: int = 2000) -> Tuple[bool, Optional[str]]:
    """Validate file size"""
    max_bytes = max_mb * 1024 * 1024
    if size_bytes > max_bytes:
        return False, f"File size exceeds {max_mb}MB limit"
    return True, None

def validate_link_id(link_id: str) -> bool:
    """Validate link ID format"""
    return bool(re.match(r'^[a-zA-Z0-9_-]{8,}$', link_id))

def validate_user_id(user_id: int) -> bool:
    """Validate Telegram user ID"""
    return isinstance(user_id, int) and user_id > 0

def validate_expiry_time(expiry: datetime) -> bool:
    """Check if expiry time is in the future"""
    return expiry > datetime.utcnow()

def calculate_expiry(days: int) -> datetime:
    """Calculate expiry datetime from days"""
    return datetime.utcnow() + timedelta(days=days)

def is_expired(expiry: datetime) -> bool:
    """Check if datetime has expired"""
    return datetime.utcnow() > expiry

def validate_channel_id(channel_id: int) -> bool:
    """Validate Telegram channel ID format"""
    # Channel IDs are negative integers starting with -100
    return isinstance(channel_id, int) and str(channel_id).startswith('-100')

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to remove dangerous characters"""
    # Remove path traversal attempts
    filename = filename.replace('..', '').replace('/', '_').replace('\\', '_')
    # Remove special characters
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    return filename[:255]  # Limit length