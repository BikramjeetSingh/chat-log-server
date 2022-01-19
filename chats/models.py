from django.contrib.auth.models import User
from django.db import models


class ChatMessage(models.Model):

    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    is_sent = models.BooleanField()
