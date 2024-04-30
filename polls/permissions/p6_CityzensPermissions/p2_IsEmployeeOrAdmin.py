from rest_framework import permissions


class IsEmployeeOrAdminSimple(permissions.BasePermission):
    """
    Custom permission to allow access to admins or the object's owner only.
    """

    def has_permission(self, request, view):

        user = request.user
        #
        # Employee
        #
        # Check if the employee's department matches the department of the object(Passport)
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
