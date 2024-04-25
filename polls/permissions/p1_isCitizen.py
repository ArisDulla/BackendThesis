from rest_framework import permissions


class IsCitizen(permissions.BasePermission):

    def has_permission(self, request, view):

        user = request.user
        #
        # Employee
        #
        # Check if is citizen's
        #
        if hasattr(user, "cityzens"):
            return True

        return False
