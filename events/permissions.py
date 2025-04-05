from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsEventOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the organizer
        return obj.organizer == request.user
    

class IsOrganizer(BasePermission):
    """
    Allow access to only users who are marked as organizers.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_organizer
    
