"""Session Manager for Telegram Accounts"""
import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime
from src.utils import EncryptionManager, get_login_logger


class SessionManager:
    """Manage multiple Telegram sessions"""

    def __init__(self, session_path: str, encryption_key: str = None):
        self.session_path = Path(session_path)
        self.session_path.mkdir(parents=True, exist_ok=True)
        self.encryption = EncryptionManager(encryption_key) if encryption_key else None
        self.logger = get_login_logger()

    def get_sessions(self) -> List[Dict]:
        """Get all saved sessions"""
        sessions = []
        metadata_file = self.session_path / "sessions_metadata.json"

        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    sessions = json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading sessions: {e}")

        return sessions

    def save_session(self, session_name: str, phone_number: str, api_id: int, api_hash: str) -> bool:
        """Save a new session metadata"""
        try:
            sessions = self.get_sessions()

            # Check if session already exists
            if any(s["name"] == session_name for s in sessions):
                self.logger.warning(f"Session {session_name} already exists")
                return False

            session_data = {
                "name": session_name,
                "phone_number": phone_number,
                "api_id": api_id,
                "api_hash": api_hash,
                "created_at": datetime.now().isoformat(),
                "last_used": datetime.now().isoformat(),
            }

            sessions.append(session_data)

            metadata_file = self.session_path / "sessions_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(sessions, f, indent=2)

            self.logger.info(f"Session {session_name} saved successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error saving session: {e}")
            return False

    def get_session(self, session_name: str) -> Optional[Dict]:
        """Get a specific session"""
        sessions = self.get_sessions()
        return next((s for s in sessions if s["name"] == session_name), None)

    def delete_session(self, session_name: str) -> bool:
        """Delete a session"""
        try:
            sessions = self.get_sessions()
            sessions = [s for s in sessions if s["name"] != session_name]

            metadata_file = self.session_path / "sessions_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(sessions, f, indent=2)

            # Delete session file if exists
            session_file = self.session_path / f"{session_name}.session"
            if session_file.exists():
                session_file.unlink()

            self.logger.info(f"Session {session_name} deleted")
            return True

        except Exception as e:
            self.logger.error(f"Error deleting session: {e}")
            return False

    def update_last_used(self, session_name: str) -> None:
        """Update last used timestamp"""
        try:
            sessions = self.get_sessions()
            for session in sessions:
                if session["name"] == session_name:
                    session["last_used"] = datetime.now().isoformat()

            metadata_file = self.session_path / "sessions_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(sessions, f, indent=2)

        except Exception as e:
            self.logger.error(f"Error updating session: {e}")

    def get_session_file_path(self, session_name: str) -> Path:
        """Get the file path for a session"""
        return self.session_path / f"{session_name}.session"
