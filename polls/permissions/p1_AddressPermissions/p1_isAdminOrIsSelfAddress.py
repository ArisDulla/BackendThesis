from rest_framework import permissions
from ...models import UserAddress
from django.shortcuts import get_object_or_404


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
        # Employee
        #
        # Check if the employee's department matches the department of the object(address of cityzen)
        #
        if hasattr(user, "employee"):

            employee = user.employee

            try:
                citizen = get_object_or_404(UserAddress, address=obj)
            except Exception:
                citizen = None

            usercx = getattr(citizen, "user", None)
            cityzens = getattr(usercx, "cityzens", None)
            departmentxx = getattr(cityzens, "department", None)

            if departmentxx is not None:

                if employee.department == departmentxx:

                    if employee.employee_type in ["YP02", "YP01", "SEC"]:

                        return True

        #
        # Allow object's owner to access.
        #
        try:
            user_addresses = get_object_or_404(UserAddress, user=user, address=obj)
        except Exception:
            return False

        if user_addresses:
            return True

        return False
