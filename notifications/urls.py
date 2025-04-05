from django.urls import path
from .views import NotificationListView, MarkAsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('<uuid:pk>/mark-as-read/', MarkAsReadView.as_view(), name='notification-mark-as-read'),
]
