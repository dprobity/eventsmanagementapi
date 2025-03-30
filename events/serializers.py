from rest_framework import serializers
from .models import Event
from django.utils import timezone

class EventSerializer(serializers.ModelSerializer):
    tickets_remaining = serializers.ReadOnlyField()
    is_selling_out_soon = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'location',
            'date_time',
            'capacity',
            'registered_count',
            'event_ticket_sells_off_soon',
            'tickets_remaining',
            'is_selling_out_soon',
            'is_active',
            'is_recurring',
            'organizer',
            'category',
            'created_at',
        ]
        read_only_fields = ['registered_count', 'tickets_remaining', 'is_selling_out_soon', 'created_at', 'organizer']

    def validate_date_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Event date and time cannot be in the past.")
        return value
