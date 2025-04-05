from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Event
from .serializers import EventSerializer
from .permissions import IsEventOwnerOrReadOnly
from .permissions import IsOrganizer



class EventCreateView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsOrganizer]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.filter(date_time__gte=timezone.now(), is_active=True)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'location']
    filterset_fields = ['category__slug', 'location']

class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

class EventUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsEventOwnerOrReadOnly]
