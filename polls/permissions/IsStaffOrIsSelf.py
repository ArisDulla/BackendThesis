from rest_framework import permissions


class IsStaffOrIsSelf(permissions.BasePermission):
    """
    Custom permission to allow access to admins or the object's owner only.
    """

    def has_object_permission(self, request, view, obj):
        # Allow admins full access.
        if request.user and request.user.is_staff:
            return True

        # Allow object's owner to access.
        return obj.user == request.user
