from django.urls import path
from .views import UserRegistrationView, UserProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('me/', UserProfileView.as_view(), name='profile'),
]
