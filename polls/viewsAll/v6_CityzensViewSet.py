from rest_framework import viewsets
from ..models import Cityzens, Department
from ..serializers.s6_CityzensSerializer import CityzensSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from ..permissions.p6_CityzensPermissions.p1_IsEmployeeOrAdmin import (
    IsEmployeeOrAdmin,
)
from ..permissions.p6_CityzensPermissions.p2_IsEmployeeOrAdmin import (
    IsEmployeeOrAdminSimple,
)
from rest_framework.decorators import action
from ..permissions.p6_CityzensPermissions.p3_IsCityzenOrAdmin import (
    IsCityzenOrAdmin,
)
from rest_framework import status
from django.shortcuts import get_object_or_404


class CityzensViewSet(viewsets.ModelViewSet):
    queryset = Cityzens.objects.all()
    serializer_class = CityzensSerializer

    #
    # FOR CITYZENS The process of creating a citizen is done through the Signal (user_activated) after successful user activation.
    #
    # DJOSER this endpoint to retrieve/update the authenticated user.
    # URL: /users/me/ ,GET, PUT and PATCH
    #

    #
    # Pass partial=True to the serializer instance
    #
    # def get_serializer(self, *args, **kwargs):
    #     kwargs["partial"] = True
    #     return super().get_serializer(*args, **kwargs)

    #
    # ONLY FOR Employees GET , PUT , POST AND DELETE
    #
    # Permission -- Check if the employee's department matches the department of the object --
    #
    def get_permissions(self):

        #
        # has_object_permission
        #
        if self.action in ["retrieve", "update", "destroy"]:
            permission_classes = [IsEmployeeOrAdmin]

        #
        # has_permission
        #
        elif self.action in ["create", "list_employee"]:
            permission_classes = [IsEmployeeOrAdminSimple]

        #
        # For cityzens - has_object_permission
        #
        elif self.action == "update_department":
            permission_classes = [IsCityzenOrAdmin]

        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    #
    # Perform create
    #
    def perform_create(self, serializer):
        user = self.request.user

        #
        # if user is employee
        #
        departmentOfEmployee = None
        if hasattr(user, "employee"):
            departmentOfEmployee = user.employee.department
        #
        # or admin user
        #
        elif user and user.is_staff:
            department_id = self.request.data.get("department")

            #
            # get instance
            #
            departmentOfEmployee = get_object_or_404(Department, pk=department_id)
            if not departmentOfEmployee:
                return Response(
                    {"message": "Department ID does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer.save(department=departmentOfEmployee)

    #
    # Perform Update
    #
    def perform_update(self, serializer):

        user = self.request.user

        #
        # FOR ADMIN
        #
        if user and user.is_staff:

            department_id = self.request.data.get("department")
            #
            # get instance
            #
            departmentOfEmployee = get_object_or_404(Department, pk=department_id)
            if not departmentOfEmployee:
                return Response(
                    {"message": "Department ID does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save(department=departmentOfEmployee)
        else:
            serializer.save()

    #
    # Override the update method
    #
    #  UPDATE - partial=True
    #
    def update(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=200)

    #
    # LIST of citizens every department
    #
    # - /api/----/list-employee/
    #
    # ACTION ONLY FOR EMPLOYEES
    #
    @action(
        detail=False,
        methods=["get"],
        url_path="list-employee",
        url_name="list_employee",
    )
    def list_employee(self, request, *args, **kwargs):

        user = request.user
        if hasattr(user, "employee"):
            queryset = self.queryset.filter(
                department=user.employee.department.id
            ).order_by("-user__created")

            serializer = self.get_serializer(queryset, many=True)

            return Response(serializer.data)
        else:
            return Response({"message": "User is not associated with any department."})

    #
    # PUT ACTION FOR Cityzens
    #
    @action(detail=True, methods=["put"])
    def update_department(self, request, pk=None):

        department_id = self.request.data.get("department")

        #
        # get instance
        #
        departmentOfEmployee = get_object_or_404(Department, pk=department_id)
        if not departmentOfEmployee:
            return Response(
                {"message": "Department ID does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance = self.get_object()
        instance.department = departmentOfEmployee
        instance.save()
        self.get_serializer(instance)

        return Response({"message": "Department updated successfully."}, status=200)
