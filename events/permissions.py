from rest_framework import permissions

class IsEventOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the organizer
        return obj.organizer == request.user
