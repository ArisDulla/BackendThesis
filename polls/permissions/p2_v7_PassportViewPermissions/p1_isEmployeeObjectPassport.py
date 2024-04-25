from rest_framework import permissions


class IsEmployeeObjectPassport(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        user = request.user
        #
        # Employee
        #
        # Check if the employee's department matches the department of the object(Passport)
        #
        if hasattr(user, "employee"):

            employee = user.employee

            if employee.department == obj.issuing_authority:

                if employee.employee_type in ["YP02"]:
                    return True
        #
        # ADMIN
        #
        # Allow admins full access.
        #
        elif user and user.is_staff:
            return True

        return False
