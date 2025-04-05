from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """
    GET /notifications/
    Lists all notifications for the authenticated user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class MarkAsReadView(generics.UpdateAPIView):
    """
    PATCH /notifications/<uuid:pk>/mark-as-read/
    Marks a single notification as read.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        # Only notifications belonging to the user
        return Notification.objects.filter(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)


