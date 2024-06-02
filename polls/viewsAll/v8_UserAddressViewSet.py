from rest_framework import viewsets
from ..models import UserAddress, CustomUser
from ..serializers.s8_UserAddressSerializer import UserAddressSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from polls.permissions.p8_UserAddressPermissions.p1_IsEmployee import IsEmployee
from polls.permissions.p8_UserAddressPermissions.p2_IsEmployeeDepartment import (
    IsEmployeeDepartment,
)
from rest_framework.exceptions import PermissionDenied
from django.http import Http404


class UserAddressViewSet(viewsets.ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer

    def get_permissions(self):
        if self.action in ["create", "list_user"]:
            permission_classes = [IsAuthenticated]

        elif self.action in ["retrieve", "update", "destroy", "list_user"]:
            permission_classes = [IsEmployeeDepartment]

        elif self.action == "list_employee":
            permission_classes = [IsEmployee]

        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    #
    # Perform Create
    #
    def perform_create(self, serializer):

        user = self.request.user

        if hasattr(user, "employee"):
            employeeDepartment = user.employee.department
            userId = self.request.data["user"]

            try:
                userRequest = get_object_or_404(CustomUser, id=userId)
            except Http404:
                raise PermissionDenied(
                    "You do not have permission to access this data."
                )
            if hasattr(userRequest, "cityzens"):
                citizenDepartment = userRequest.cityzens.department

                #
                # Same Department
                #
                if citizenDepartment == employeeDepartment:
                    user = userRequest
                else:
                    raise PermissionDenied(
                        "You do not have permission to access this data."
                    )
        if user.is_staff:

            userId = self.request.data["user"]
            user = get_object_or_404(CustomUser, id=userId)

        serializer.save(user=user)

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

    @action(
        detail=False,
        methods=["get"],
        url_name="list-employee",
        url_path=r"list-employee/(?P<userId>\w+)",
    )
    def list_employee(self, request, userId=None):

        #
        # Employee Department
        #
        employeeDepartment = request.user.employee.department

        #
        # Citizen Department
        #
        try:
            user = get_object_or_404(CustomUser, id=userId)
        except Http404:
            raise PermissionDenied("You do not have permission to access this data.")

        if hasattr(user, "cityzens"):
            citizenDepartment = user.cityzens.department

            #
            # Same Department
            #
            if citizenDepartment == employeeDepartment:

                user_addresses = self.queryset.filter(user=user)
                serializer = self.get_serializer(user_addresses, many=True)
                return Response(serializer.data)

            else:
                # The citizen's department does not match the employee's department.
                raise PermissionDenied(
                    "You do not have permission to access this data."
                )

        else:
            raise PermissionDenied("You do not have permission to access this data.")

    #
    # List for citizens
    #
    @action(
        detail=False,
        methods=["get"],
        url_path="list-user",
        url_name="list_user",
    )
    def list_user(self, request, *args, **kwargs):

        user = request.user

        user_addresses = self.queryset.filter(user=user)
        serializer = self.get_serializer(user_addresses, many=True)
        return Response(serializer.data)
