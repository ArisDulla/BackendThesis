from rest_framework import permissions


class IsCityzenOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow access to admins or the object's owner only.
    """

    def has_object_permission(self, request, view, obj):

        user = request.user

        #
        # For Citizens
        #
        if hasattr(user, "cityzens"):

            cityzen = user.cityzens

            if cityzen == obj:
                return True

        #
        # ADMIN
        #
        # Allow admins full access.
        #
        elif user and user.is_staff:

            return True

        return False
