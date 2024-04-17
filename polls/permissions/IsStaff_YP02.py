from rest_framework import permissions


class IsStaff_YP02(permissions.BasePermission):

    def has_permission(self, request, view):

        if hasattr(request.user, "employee"):
            if request.user.employee.employee_type == "YP02":
                return True

        return False
