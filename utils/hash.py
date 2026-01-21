import hashlib
import secrets
import string
from typing import Optional

def generate_file_hash(file_data: bytes) -> str:
    """Generate SHA256 hash of file data"""
    return hashlib.sha256(file_data).hexdigest()

def generate_short_hash(length: int = 8) -> str:
    """Generate short random hash for links"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_secure_token(length: int = 32) -> str:
    """Generate secure random token"""
    return secrets.token_urlsafe(length)

def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hashed

def generate_link_id() -> str:
    """Generate unique link ID"""
    return generate_short_hash(12)

def generate_file_id() -> str:
    """Generate unique file ID"""
    return generate_secure_token(16)