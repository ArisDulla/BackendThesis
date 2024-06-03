from rest_framework import permissions


class IsEmployee(permissions.BasePermission):
    """
    Custom permission to allow access to admins or the object's owner only.
    """

    def has_permission(self, request, view):

        user = request.user
        #
        # Employee
        #
        if hasattr(user, "employee"):

            employee = user.employee

            if employee.employee_type in ["YP02", "YP01", "SEC"]:
                return True

        #
        # ADMIN
        #
        # Allow admins full access.
        #
        elif user and user.is_staff:

            return True

        return False
