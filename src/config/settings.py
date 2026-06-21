"""Application Settings and Configuration"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application configuration settings"""

    # Application Info
    app_name: str = Field(default="Telegram Content Compliance Analyzer", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")

    # Telegram API Credentials
    telegram_api_id: int = Field(default=0, env="TELEGRAM_API_ID")
    telegram_api_hash: str = Field(default="", env="TELEGRAM_API_HASH")

    # OpenAI Configuration
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4-turbo-preview", env="OPENAI_MODEL")
    analysis_timeout: int = Field(default=30, env="ANALYSIS_TIMEOUT")

    # Paths
    storage_path: str = Field(default="./storage", env="STORAGE_PATH")
    log_path: str = Field(default="./storage/logs", env="LOG_PATH")
    session_path: str = Field(default="./storage/sessions", env="SESSION_PATH")
    evidence_path: str = Field(default="./storage/evidence", env="EVIDENCE_PATH")
    export_path: str = Field(default="./storage/exports", env="EXPORT_PATH")
    cache_path: str = Field(default="./storage/cache", env="CACHE_PATH")

    # Encryption
    session_encryption_key: Optional[str] = Field(default=None, env="SESSION_ENCRYPTION_KEY")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )

    # Performance
    max_messages_per_scan: int = Field(default=5000, env="MAX_MESSAGES_PER_SCAN")
    batch_size: int = Field(default=100, env="BATCH_SIZE")
    worker_threads: int = Field(default=4, env="WORKER_THREADS")

    # Security
    enable_audit_log: bool = Field(default=True, env="ENABLE_AUDIT_LOG")
    enable_encryption: bool = Field(default=True, env="ENABLE_ENCRYPTION")

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **data):
        # Load .env file if it exists
        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)

        super().__init__(**data)

        # Create required directories
        self._create_directories()

    def _create_directories(self):
        """Create required storage directories"""
        paths = [
            self.storage_path,
            self.log_path,
            self.session_path,
            self.evidence_path,
            self.export_path,
            self.cache_path,
        ]

        for path in paths:
            Path(path).mkdir(parents=True, exist_ok=True)

    def validate_credentials(self) -> tuple[bool, str]:
        """Validate required credentials"""
        if not self.telegram_api_id or self.telegram_api_id == 0:
            return False, "Telegram API ID not configured"

        if not self.telegram_api_hash:
            return False, "Telegram API Hash not configured"

        if not self.openai_api_key:
            return False, "OpenAI API Key not configured"

        return True, "All credentials configured"


# Global settings instance
settings = Settings()
