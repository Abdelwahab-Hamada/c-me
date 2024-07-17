from django.contrib import admin
from .models import ChatMessage, Chat, MessageAttachment


class ChatMessageAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified',)
    search_fields = ('id', 'text', 'sender__pk', 'chat__pk')
    list_display = ('id', 'sender', 'chat', 'text', 'read')
    list_display_links = ('id',)
    list_filter = ('sender', 'chat')
    date_hierarchy = 'created'


class ChatAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified',)
    search_fields = ('id', 'user1__pk', 'user2__pk')
    list_display = ('id', 'user1', 'user2')
    list_display_links = ('id',)
    date_hierarchy = 'created'


admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(MessageAttachment)