import uuid
from django.db import models
from django.conf import settings
from events.models import Event

class Notification(models.Model):
    """
    A simple model for in-app notifications:
    - Linked to a specific user
    - Optionally linked to an event
    - Contains a message
    - Tracks read/unread status
    - Has a created_at timestamp
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email} - {self.message[:30]}"
