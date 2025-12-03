from django.db import models
from django.utils import timezone
from accounts.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    target_users = models.ManyToManyField(User, related_name='received_messages', blank=True)
    is_broadcast = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.created_at}"
