from pyrogram import Client
from pyrogram.types import Message
from typing import Optional
from config import config
import asyncio

class ChannelManager:
    """Manage file storage in Telegram channel"""
    
    def __init__(self, client: Client):
        self.client = client
        self.channel_id = config.STORAGE_CHANNEL_ID
    
    async def upload_file(self, file_path: str, caption: Optional[str] = None) -> Optional[Message]:
        """Upload file to storage channel"""
        try:
            message = await self.client.send_document(
                chat_id=self.channel_id,
                document=file_path,
                caption=caption
            )
            return message
        except Exception as e:
            print(f"Error uploading to channel: {e}")
            return None
    
    async def get_file(self, message_id: int) -> Optional[Message]:
        """Get file message from channel"""
        try:
            message = await self.client.get_messages(
                chat_id=self.channel_id,
                message_ids=message_id
            )
            return message
        except Exception as e:
            print(f"Error getting file from channel: {e}")
            return None
    
    async def forward_file(self, message_id: int, to_chat_id: int) -> Optional[Message]:
        """Forward file from channel to user"""
        try:
            message = await self.client.forward_messages(
                chat_id=to_chat_id,
                from_chat_id=self.channel_id,
                message_ids=message_id
            )
            return message[0] if isinstance(message, list) else message
        except Exception as e:
            print(f"Error forwarding file: {e}")
            return None
    
    async def copy_file(self, message_id: int, to_chat_id: int, caption: Optional[str] = None) -> Optional[Message]:
        """Copy file from channel to user"""
        try:
            message = await self.client.copy_message(
                chat_id=to_chat_id,
                from_chat_id=self.channel_id,
                message_id=message_id,
                caption=caption
            )
            return message
        except Exception as e:
            print(f"Error copying file: {e}")
            return None
    
    async def delete_file(self, message_id: int) -> bool:
        """Delete file from channel"""
        try:
            await self.client.delete_messages(
                chat_id=self.channel_id,
                message_ids=message_id
            )
            return True
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    async def verify_channel_access(self) -> bool:
        """Verify bot has access to storage channel"""
        try:
            chat = await self.client.get_chat(self.channel_id)
            return True
        except Exception as e:
            print(f"❌ Cannot access storage channel: {e}")
            return False