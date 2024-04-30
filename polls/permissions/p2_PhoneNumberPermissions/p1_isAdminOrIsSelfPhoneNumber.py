from rest_framework import permissions
from ...models import UserPhoneNumber
from django.shortcuts import get_object_or_404


class IsAdminOrIsSelfNumber(permissions.BasePermission):
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
        # Check if the employee's department matches the department of the object(phoneNumber of cityzen)
        #
        if hasattr(user, "employee"):

            employee = user.employee

            try:
                citizen = get_object_or_404(UserPhoneNumber, phoneNumber=obj)
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
            user_phoneNumber = get_object_or_404(
                UserPhoneNumber, user=user, phoneNumber=obj
            )
        except Exception:
            return False

        if user_phoneNumber:
            return True

        return False
