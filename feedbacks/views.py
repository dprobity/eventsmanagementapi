from rest_framework import generics, permissions
from .models import Feedback
from .serializers import FeedbackSerializer

class FeedbackListCreateView(generics.ListCreateAPIView):
    """
    GET: List all feedbacks or filter by event
    POST: Create a new feedback
    """
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Feedback.objects.all()
        event_id = self.request.query_params.get('event')
        if event_id:
            queryset = queryset.filter(event__id=event_id)
        return queryset

    def perform_create(self, serializer):
        # Force the 'user' to be the one creating feedback
        serializer.save(user=self.request.user)

class FeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve single feedback
    PUT/PATCH: Update feedback (only if you're the owner or admin)
    DELETE: Delete feedback
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        # Ensure only the feedback owner or admin can update
        feedback = self.get_object()
        if self.request.user != feedback.user and not self.request.user.is_staff:
            raise PermissionError("You cannot update another user's feedback.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.user and not self.request.user.is_staff:
            raise PermissionError("You cannot delete another user's feedback.")
        instance.delete()
