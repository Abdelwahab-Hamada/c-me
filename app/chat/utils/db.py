from channels.db import database_sync_to_async
from ..models import ChatMessage

@database_sync_to_async
def save_text_message(sender, chat, text):
    return ChatMessage.objects.create(text=text, sender_id=sender, chat_id=chat)