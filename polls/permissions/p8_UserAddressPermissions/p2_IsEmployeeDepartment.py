from rest_framework import permissions


class IsEmployeeDepartment(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        user = request.user

        #
        # Employee
        #
        if hasattr(user, "employee"):

            employee = user.employee

            #
            # Employee
            #
            if employee.employee_type in ["YP02", "YP01", "SEC"]:

                if hasattr(obj.user, "cityzens"):

                    userDepartment = obj.user.cityzens.department
                    employeeDepartment = employee.department

                    if userDepartment and employeeDepartment:

                        #
                        # Check if the employee's department matches the department of the object
                        #
                        if userDepartment == employeeDepartment:

                            return True

        #
        # ADMIN
        #
        # Allow admins full access.
        #
        elif user and user.is_staff:

            return True
        #
        # Allow object's owner to access.
        #
        return obj.user == user
