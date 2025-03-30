import uuid
from django.db import models
from django.conf import settings 
from categories.models import Category
from django.utils import timezone




class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    date_time = models.DateTimeField()
    capacity = models.PositiveBigIntegerField()
    registered_count = models.PositiveBigIntegerField(default=0)
    event_ticket_sells_off_soon = models.PositiveBigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_recurring = models.BooleanField(default=False)

    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.date_time})"
    

    @property
    def tickets_remaining(self):
        return self.capacity - self.registered_count
    
    @property
    def is_selling_out_soon(self):
        if self.event_ticket_sells_off_soon is not None:
            return self.tickets_remaining <= self.event_ticket_sells_off_soon
        return False


