from rest_framework import serializers
from .models import Feedback
from django.utils import timezone

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'event', 'comment', 'rating', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

    def validate_rating(self, value):
        # Optional: ensure rating is within 1-5
        if value and (value < 1 or value > 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


    

    def validate(self, attrs):
        """Enforce these rules:
        1. User must have a successful registration (status='registered') for the event.
        2. Event date_time must be in the past (i.e., feedback is only allowed post-event) """

        
        request = self.context.get('request')
        user = request.user if request else None
        event = attrs.get('event')

        # 1) Ensure user is authenticated
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("You must be logged in to leave feedback.")

        # 2) Check that the user actually registered for this event
        from registrations.models import EventRegistration  # import here to avoid circular imports
        has_registered = EventRegistration.objects.filter(
            user=user,
            event=event,
            status='registered'
        ).exists()

        if not has_registered:
            raise serializers.ValidationError("You can only leave feedback if you have registered for this event.")

        # 3) Check that the event has actually occurred (optional)
        if event.date_time > timezone.now():
            raise serializers.ValidationError("Feedback can only be left for events that have ended.")

        return attrs
