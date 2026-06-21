"""Encryption utilities"""
import os
import secrets
from cryptography.fernet import Fernet
from pathlib import Path


class EncryptionManager:
    """Manage encryption for sessions and sensitive data"""

    def __init__(self, encryption_key: str = None):
        """Initialize encryption manager"""
        if encryption_key:
            self.key = encryption_key.encode()
        else:
            # Generate a new key
            self.key = Fernet.generate_key()

        self.cipher = Fernet(self.key)

    @staticmethod
    def generate_key() -> str:
        """Generate a new encryption key"""
        return Fernet.generate_key().decode()

    def encrypt(self, data: str) -> str:
        """Encrypt data"""
        encrypted = self.cipher.encrypt(data.encode())
        return encrypted.decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data"""
        decrypted = self.cipher.decrypt(encrypted_data.encode())
        return decrypted.decode()

    def encrypt_file(self, file_path: str) -> None:
        """Encrypt a file in place"""
        with open(file_path, 'rb') as f:
            data = f.read()

        encrypted = self.cipher.encrypt(data)

        with open(file_path, 'wb') as f:
            f.write(encrypted)

    def decrypt_file(self, file_path: str) -> bytes:
        """Decrypt a file and return contents"""
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()

        decrypted = self.cipher.decrypt(encrypted_data)
        return decrypted
