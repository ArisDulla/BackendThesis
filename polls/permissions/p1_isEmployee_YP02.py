from rest_framework import permissions


class IsEmployee_YP02(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        user = request.user
        #
        # Employee
        #
        # Check if the employee's department matches the department of the object(Application)
        #
        if hasattr(user, "employee"):

            employee = user.employee
            if employee.department == obj.departmentx:

                if employee.employee_type == "YP02":
                    return True

        #
        # ADMIN
        #
        # Allow admins full access.
        #
        elif user and user.is_staff:
            return True

        return False
