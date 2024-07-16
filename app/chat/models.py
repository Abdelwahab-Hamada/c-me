from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.db.models import Q
import uuid
import os

UserModel = get_user_model()

def user_directory_path(instance, filename):
    _, extension = os.path.splitext(filename)
    return f'{instance.id}/{uuid.uuid4()}{extension}'

class Chat(TimeStampedModel):
    id = models.BigAutoField(primary_key=True, verbose_name=_("Id"))
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User1"),
                              related_name="chats_as_user1", db_index=True)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User2"),
                              related_name="chats_as_user2", db_index=True)

    class Meta:
        unique_together = (('user1', 'user2'),)
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"

    @staticmethod
    def _exists(u1, u2):
        return Chat.objects.filter(Q(user1=u1, user2=u2) | Q(user1=u2, user2=u1)).first()

    @staticmethod
    def create_if_not_exists(u1, u2):
        chat = Chat._exists(u1, u2)
        if not chat:
            chat = Chat.objects.create(user1=u1, user2=u2)
        return chat

    @staticmethod
    def get_chats_for_user(user):
        return Chat.objects.filter(Q(user1=user) | Q(user2=user))

class ChatMessage(TimeStampedModel, SoftDeletableModel):
    id = models.BigAutoField(primary_key=True, verbose_name=_("Id"))
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Author"),
                               related_name='sent_messages', db_index=True)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_("Text"), blank=True)
    read = models.BooleanField(verbose_name=_("Read"), default=False)

    @staticmethod
    def get_unread_count_for_chat_with_user(sender, chat):
        return ChatMessage.objects.filter(sender=sender, chat=chat, read=False).count()

    @staticmethod
    def get_last_message_for_chat(chat):
        return ChatMessage.objects.filter(chat=chat).order_by('-created').first()

    @staticmethod
    def create_first_message(sender, recipient, text=None):
        chat = Chat.create_if_not_exists(sender, recipient)
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
    file = models.FileField(verbose_name=_("File"), upload_to=user_directory_path)
    message = models.ForeignKey(ChatMessage, related_name='attachments', on_delete=models.CASCADE,
                                blank=True, null=True)

    @staticmethod
    def create_message_attachment(sender, recipient, file, text=None):
        message = ChatMessage.create_first_message(sender=sender, recipient=recipient, text=text)
        MessageAttachment.objects.create(file=file, message=message)

    def __str__(self):
        return str(self.file.name)
