from rest_framework import permissions


class IsEmployeeOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow access to admins or the object's owner only.
    """

    def has_object_permission(self, request, view, obj):

        user = request.user
        #
        # Employee
        #
        # Check if the employee's department matches the department of the object(Cityzen)
        #
        if hasattr(user, "employee"):

            employee = user.employee

            if employee.department == obj.department:

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
