from rest_framework import generics, permissions
from .models import EventRegistration
from .serializers import EventRegistrationSerializer

class RegisterForEventView(generics.CreateAPIView):
    """
    POST /registrations/
    {
      "event": "event_uuid",
      "quantity": 3
    }
    Creates a new registration, generating multiple TicketInstance codes.
    """
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Force the 'user' field to be the current logged-in user
        serializer.save(user=self.request.user)

class MyRegistrationsView(generics.ListAPIView):
    """
    GET /registrations/mine/
    Lists all registrations (and tickets) belonging to the current user.
    """
    serializer_class = EventRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EventRegistration.objects.filter(user=self.request.user)
