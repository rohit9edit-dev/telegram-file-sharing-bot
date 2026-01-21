from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import base64
from typing import Tuple
from config import config

class EncryptionService:
    """Handle file encryption and decryption"""
    
    def __init__(self):
        self.key = self._derive_key(config.ENCRYPTION_KEY)
        self.cipher = Fernet(self.key)
    
    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from password"""
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'telegram_file_bot_salt',  # In production, use random salt per file
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_data(self, data: bytes) -> bytes:
        """Encrypt data"""
        return self.cipher.encrypt(data)
    
    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Decrypt data"""
        return self.cipher.decrypt(encrypted_data)
    
    def encrypt_file(self, file_path: str, output_path: str) -> bool:
        """Encrypt file and save to output path"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            encrypted = self.encrypt_data(data)
            
            with open(output_path, 'wb') as f:
                f.write(encrypted)
            
            return True
        except Exception as e:
            print(f"Encryption error: {e}")
            return False
    
    def decrypt_file(self, encrypted_path: str, output_path: str) -> bool:
        """Decrypt file and save to output path"""
        try:
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted = self.decrypt_data(encrypted_data)
            
            with open(output_path, 'wb') as f:
                f.write(decrypted)
            
            return True
        except Exception as e:
            print(f"Decryption error: {e}")
            return False

encryption_service = EncryptionService()