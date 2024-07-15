from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model
from typing import Optional, Any
from django.db.models import Q
import uuid
import os


UserModel: AbstractBaseUser = get_user_model()

def user_directory_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return settings.DEFAULT_FILES_PATH.format(uuid=instance.id, extension=extension)

class Chat(TimeStampedModel):
    id = models.BigAutoField(primary_key=True, verbose_name=_("Id"))
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User1"),
                              related_name="+", db_index=True)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User2"),
                              related_name="+", db_index=True)

    class Meta:
        unique_together = (('user1', 'user2'), ('user2', 'user1'))
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")

    def __str__(self):
        return _("Chat between ") + f"{self.user1_id}, {self.user2_id}"

    @staticmethod
    def _exists(u1: AbstractBaseUser, u2: AbstractBaseUser) -> Optional[Any]:
        return Chat.objects.filter(Q(user1=u1, user2=u2) | Q(user1=u2, user2=u1)).first()

    @staticmethod
    def create_if_not_exists(u1: AbstractBaseUser, u2: AbstractBaseUser):
        chat = Chat._exists(u1, u2)
        if not chat:
            chat = Chat.objects.create(user1=u1, user2=u2)

        return chat

    @staticmethod
    def get_chats_for_user(user: AbstractBaseUser):
        return Chat.objects.filter(Q(user1=user) | Q(user2=user))


class ChatMessage(TimeStampedModel, SoftDeletableModel):
    id = models.BigAutoField(primary_key=True, verbose_name=_("Id"))
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Author"),
                               related_name='from_user', db_index=True)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_("Text"), blank=True)
    read = models.BooleanField(verbose_name=_("Read"), default=False)
    all_objects = models.Manager()

    @staticmethod
    def get_unread_count_for_chat_with_user(sender, chat):
        return ChatMessage.objects.filter(sender_id=sender, chat_id=chat, read=False).count()

    @staticmethod
    def get_last_message_for_chat(chat):
        return ChatMessage.objects.filter(chat_id=chat).select_related('sender', 'chat').first()

    @staticmethod
    def create_first_message(sender: AbstractBaseUser, recipient: AbstractBaseUser, text: str=None):
        chat = Chat.create_if_not_exists(self.sender, self.recipient)
        message = ChatMessage.objects.create(sender=sender, chat=chat, text=text)

        return message

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ('-created',)
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

 
class MessageAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    file = models.FileField(verbose_name=_("File"), blank=False, null=False, upload_to=user_directory_path)
    message = models.ForeignKey(ChatMessage, related_name='file', on_delete=models.CASCADE,
                            blank=True, null=True)

    @staticmethod
    def create_first_message_attachment(sender: AbstractBaseUser, recipient: AbstractBaseUser, file, text: str=None):
        message = ChatMessage.create_first_message(sender=sender, recipient=recipient, text=text)
        MessageAttachment.objects.create(file=file, message=message)

    def __str__(self):
        return str(self.file.name)