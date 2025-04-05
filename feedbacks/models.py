import uuid
from django.db import models
from django.conf import settings
from events.models import Event

class Feedback(models.Model):
    """
    A model for storing feedback or reviews on an event.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )

    comment = models.TextField(blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True)  # e.g., scale of 1-5

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.email} on {self.event.title}"
