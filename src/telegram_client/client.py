"""Telegram Client Wrapper using Telethon"""
import asyncio
from typing import Optional, List, Dict
from telethon import TelegramClient as TelethonClient
from telethon.tl.types import Channel, Chat, User, Message
from pathlib import Path
from src.utils import get_login_logger, get_scan_logger


class TelegramClient:
    """Wrapper around Telethon for Telegram API access"""

    def __init__(self, api_id: int, api_hash: str, session_path: str, session_name: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.session_path = Path(session_path)
        self.session_name = session_name
        self.client = None
        self.is_connected = False
        self.logger = get_login_logger()
        self.scan_logger = get_scan_logger()

    async def connect(self) -> bool:
        """Connect to Telegram"""
        try:
            session_file = self.session_path / self.session_name
            self.client = TelethonClient(
                str(session_file),
                self.api_id,
                self.api_hash
            )

            await self.client.connect()
            self.is_connected = True
            self.logger.info("Connected to Telegram")
            return True

        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from Telegram"""
        if self.client:
            await self.client.disconnect()
            self.is_connected = False
            self.logger.info("Disconnected from Telegram")

    async def is_user_authorized(self) -> bool:
        """Check if user is authorized"""
        try:
            if not self.client:
                return False
            return await self.client.is_user_authorized()
        except Exception as e:
            self.logger.error(f"Authorization check error: {e}")
            return False

    async def send_code_request(self, phone_number: str) -> bool:
        """Request OTP code"""
        try:
            if not self.client:
                return False

            await self.client.send_code_request(phone_number)
            self.logger.info(f"Code requested for {phone_number}")
            return True

        except Exception as e:
            self.logger.error(f"Code request error: {e}")
            return False

    async def sign_in(self, phone_number: str, code: str, password: str = None) -> bool:
        """Sign in with phone and code"""
        try:
            if not self.client:
                return False

            await self.client.sign_in(phone_number, code, password)
            self.logger.info(f"Successfully signed in: {phone_number}")
            return True

        except Exception as e:
            self.logger.error(f"Sign in error: {e}")
            return False

    async def get_me(self) -> Optional[Dict]:
        """Get current user information"""
        try:
            if not self.client:
                return None

            me = await self.client.get_me()
            return {
                "id": me.id,
                "is_bot": me.bot,
                "first_name": me.first_name,
                "last_name": me.last_name or "",
                "username": me.username or "",
                "phone": me.phone or "",
            }

        except Exception as e:
            self.logger.error(f"Get me error: {e}")
            return None

    async def get_dialogs(self, limit: int = 100) -> List[Dict]:
        """Get all dialogs (channels, groups, chats)"""
        try:
            if not self.client:
                return []

            dialogs = []
            async for dialog in self.client.iter_dialogs(limit=limit):
                entity = dialog.entity

                dialog_info = {
                    "id": dialog.id,
                    "name": dialog.title,
                    "type": self._get_entity_type(entity),
                    "members": 0,
                    "is_group": dialog.is_group,
                    "is_channel": dialog.is_channel,
                    "is_user": dialog.is_user,
                    "unread_count": dialog.unread_count,
                }

                # Get member count
                if hasattr(entity, "participants_count"):
                    dialog_info["members"] = entity.participants_count
                elif hasattr(entity, "member_count"):
                    dialog_info["members"] = entity.member_count

                dialogs.append(dialog_info)

            self.scan_logger.info(f"Retrieved {len(dialogs)} dialogs")
            return dialogs

        except Exception as e:
            self.logger.error(f"Get dialogs error: {e}")
            return []

    async def get_messages(
        self,
        entity_id: int,
        limit: int = 100,
        offset_id: int = 0,
        max_id: int = 0,
        min_id: int = 0,
    ) -> List[Dict]:
        """Get messages from a channel/group"""
        try:
            if not self.client:
                return []

            messages = []
            async for message in self.client.iter_messages(
                entity_id,
                limit=limit,
                offset_id=offset_id,
                max_id=max_id,
                min_id=min_id,
            ):
                msg_data = {
                    "id": message.id,
                    "date": message.date.isoformat() if message.date else None,
                    "text": message.text or "",
                    "sender_id": message.sender_id,
                    "is_reply": message.is_reply,
                    "views": message.views or 0,
                    "forwards": message.forwards or 0,
                    "has_media": message.media is not None,
                    "media_type": self._get_media_type(message.media),
                    "file_size": self._get_file_size(message.media),
                }

                # Get sender info
                if message.sender_id:
                    try:
                        sender = await self.client.get_entity(message.sender_id)
                        if isinstance(sender, User):
                            msg_data["sender_name"] = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
                            msg_data["sender_username"] = sender.username or ""
                    except:
                        pass

                messages.append(msg_data)

            self.scan_logger.info(f"Retrieved {len(messages)} messages from entity {entity_id}")
            return messages

        except Exception as e:
            self.logger.error(f"Get messages error: {e}")
            return []

    @staticmethod
    def _get_entity_type(entity) -> str:
        """Determine entity type"""
        if isinstance(entity, Channel):
            return "Channel"
        elif isinstance(entity, Chat):
            return "Group"
        elif isinstance(entity, User):
            return "User"
        return "Unknown"

    @staticmethod
    def _get_media_type(media) -> Optional[str]:
        """Get media type"""
        if not media:
            return None

        media_type = type(media).__name__
        return media_type

    @staticmethod
    def _get_file_size(media) -> int:
        """Get file size from media"""
        if not media:
            return 0

        if hasattr(media, "document") and hasattr(media.document, "size"):
            return media.document.size

        return 0

    async def download_media(self, message: Message, download_path: str) -> Optional[str]:
        """Download media from message"""
        try:
            if not message.media:
                return None

            if not self.client:
                return None

            path = await self.client.download_media(message, download_path)
            self.scan_logger.info(f"Downloaded media to {path}")
            return path

        except Exception as e:
            self.logger.error(f"Download media error: {e}")
            return None
