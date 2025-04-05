import random
import string
from rest_framework import serializers
from django.utils import timezone
from events.models import Event
from .models import EventRegistration, TicketInstance
from notifications.models import Notification  # <-- import Notification model

class TicketInstanceSerializer(serializers.ModelSerializer):
    """
    A read-only serializer for the individual tickets.
    We won't allow creating them manually; they get created automatically.
    """
    class Meta:
        model = TicketInstance
        fields = ['id', 'code', 'is_used']

class EventRegistrationSerializer(serializers.ModelSerializer):
    """
    Handles creating a new registration (bulk order) for an event,
    plus generating multiple TicketInstance records.
    """

    # Show nested ticket data in the response, read-only
    ticket_instances = TicketInstanceSerializer(many=True, read_only=True)

    class Meta:
        model = EventRegistration
        fields = [
            'id',
            'user',
            'event',
            'quantity',
            'status',
            'is_waitlisted',
            'created_at',
            'ticket_instances',
        ]
        read_only_fields = [
            'status',
            'is_waitlisted',
            'created_at',
            'ticket_instances',
        ]

    def validate(self, attrs):
        """
        Basic validation before creation:
        - Ensure the event is not in the past (optional).
        - Ensure quantity >= 1.
        - (Optional) Check if user already registered for this event (unique_together).
        """
        event = attrs.get('event')
        quantity = attrs.get('quantity', 1)

        # Optional: block registering for events in the past
        if event.date_time < timezone.now():
            raise serializers.ValidationError("Cannot register for a past event.")

        if quantity < 1:
            raise serializers.ValidationError("You must buy at least 1 ticket.")

        return attrs

    def create(self, validated_data):
        """
        Core logic to handle:
        1. Checking event capacity vs. quantity requested.
        2. If not enough capacity -> waitlist. Otherwise, increment `registered_count`.
        3. Generate a ticket code for each seat (TicketInstance).
        4. Create a Notification about the registration status.
        """
        event = validated_data['event']
        quantity = validated_data['quantity']
        user = validated_data['user']  # because user is set via perform_create()

        # Check capacity
        if event.registered_count + quantity <= event.capacity:
            validated_data['status'] = 'registered'
            validated_data['is_waitlisted'] = False
            event.registered_count += quantity
            event.save()
        else:
            validated_data['status'] = 'waitlisted'
            validated_data['is_waitlisted'] = True

        # Create the main registration record
        registration = super().create(validated_data)

        # Generate a unique code for *each* ticket
        for i in range(quantity):
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            ticket_code = f"EVT-{random_part}-{i+1}"

            TicketInstance.objects.create(
                registration=registration,
                code=ticket_code
            )

        # ─────────────────────────────────────────────────────
        #  Create a Notification after registration is saved
        # ─────────────────────────────────────────────────────
        if registration.status == 'registered':
            message = f"You have successfully registered for {event.title}!"
        else:
            message = f"You have been waitlisted for {event.title}."

        Notification.objects.create(
            user=user,
            event=event,
            message=message
        )

        return registration
