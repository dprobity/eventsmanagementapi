from django.urls import path
from .views import (
    EventCreateView,
    EventListView,
    EventDetailView,
    EventUpdateDeleteView,
)

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('<uuid:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('<uuid:pk>/edit/', EventUpdateDeleteView.as_view(), name='event-update-delete'),
]
