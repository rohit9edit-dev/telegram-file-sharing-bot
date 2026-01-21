from typing import Optional
from utils.encryption import encryption_service
from utils.hash import hash_password, verify_password
import secrets

class SecurityService:
    """Service for security operations"""
    
    def __init__(self):
        self.encryption = encryption_service
    
    def encrypt_file(self, input_path: str, output_path: str) -> bool:
        """Encrypt a file"""
        return self.encryption.encrypt_file(input_path, output_path)
    
    def decrypt_file(self, input_path: str, output_path: str) -> bool:
        """Decrypt a file"""
        return self.encryption.decrypt_file(input_path, output_path)
    
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return hash_password(password)
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password"""
        return verify_password(password, hashed)
    
    def generate_access_token(self, length: int = 32) -> str:
        """Generate a secure access token"""
        return secrets.token_urlsafe(length)
    
    def validate_channel_access(self, channel_id: int) -> bool:
        """Validate bot has access to channel"""
        from config import config
        return channel_id == config.STORAGE_CHANNEL_ID

security_service = SecurityService()