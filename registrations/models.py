import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from events.models import Event


class EventRegistration(models.Model):
    """
    Each record represents one 'bulk registration' or 'order' for an event,
    which can include multiple tickets.
    """
    STATUS_CHOICES = (
        ('registered', 'Registered'),
        ('cancelled', 'Cancelled'),
        ('waitlisted', 'Waitlisted'),
    )

    # Primary key as a UUID for global uniqueness
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Which user is registering
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations'
    )

    # Which event the user is registering for
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )

    # Quantity of tickets the user wants to buy in a single registration
    quantity = models.PositiveIntegerField(default=1)

    # Registration status: 'registered', 'waitlisted', or 'cancelled'
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='registered'
    )

    # Quick boolean to indicate if the user is on the waitlist
    is_waitlisted = models.BooleanField(default=False)

    # Timestamp for when this registration was created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent a single user from registering multiple times for the same event
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.email} -> {self.event.title} [{self.status}]"


class TicketInstance(models.Model):
    """
    Each record represents an *individual ticket* within an EventRegistration.
    Useful if you want separate ticket codes for each seat or each attendee.
    """
    # Primary key as a UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Link back to the parent EventRegistration
    registration = models.ForeignKey(
        EventRegistration,
        on_delete=models.CASCADE,
        related_name='ticket_instances'
    )

    # A unique code for scanning or verifying the ticket (e.g., "EVT-ABCD1234-1")
    code = models.CharField(max_length=50, unique=True)

    # True if the ticket has been used/scanned at the event check-in
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Ticket {self.code} for {self.registration.event.title}"
