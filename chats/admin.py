from django.contrib import admin

from chats.models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):

    list_display = [
        'user',
        'content',
        'timestamp',
        'is_sent',
    ]
