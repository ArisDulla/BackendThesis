from rest_framework import permissions


class IsStaff_YP01(permissions.BasePermission):

    def has_permission(self, request, view):

        if hasattr(request.user, "employee"):
            if request.user.employee.employee_type == "YP01":
                return True

        return False
