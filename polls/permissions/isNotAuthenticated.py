from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsNotAuthenticated(BasePermission):
    """
    Custom permission to allow access only if the user is not authenticated.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            raise PermissionDenied("You are already logged in.")
        return True
