from rest_framework import permissions
from ...models import UserAddress


class IsAdminOrIsSelfAddress(permissions.BasePermission):
    """
    Custom permission to allow access to admins or the object's owner only.
    """

    def has_object_permission(self, request, view, obj):

        user = request.user

        #
        # ADMIN
        #
        # Allow admins full access.
        #
        if user and user.is_staff:

            return True

        #
        # Allow object's owner to access.
        #
        user_addresses = UserAddress.objects.filter(user=user, address=obj)

        return user_addresses.exists()
