from rest_framework import permissions


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):

        if hasattr(request.user, "employee"):
            if request.user.employee.employee_type in ["YP01", "YP02"]:
                return True

        return False
