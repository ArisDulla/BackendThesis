from rest_framework import permissions


class IsEmployeePassport(permissions.BasePermission):

    def has_permission(self, request, view):

        user = request.user

        #
        # Employee
        #
        if hasattr(user, "employee"):

            if user.employee.employee_type == "YP02":
                return True

        return False
