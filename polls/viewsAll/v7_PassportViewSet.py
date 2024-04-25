from rest_framework import viewsets
from ..models import Passport
from ..serializers.s7_PassportSerializer import PassportSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from ..permissions.p2_v7_PassportViewPermissions.p1_isEmployeeObjectPassport import (
    IsEmployeeObjectPassport,
)
from ..permissions.p2_v7_PassportViewPermissions.p2_isEmployeeOrIsSelfPassport import (
    IsEmployeeOrIsSelfPassport,
)
from ..permissions.p2_v7_PassportViewPermissions.p3_isEmployeePassport import (
    IsEmployeePassport,
)
from django.shortcuts import get_object_or_404
from polls.models import PassportApplication
from rest_framework.exceptions import PermissionDenied
from ..permissions.p1_isCitizen import IsCitizen
import random
import string


class PassportViewSet(viewsets.ModelViewSet):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer

    def get_permissions(self):

        if self.action == "update":
            permission_classes = [IsEmployeeObjectPassport]

        elif self.action == "retrieve":
            permission_classes = [IsEmployeeOrIsSelfPassport]

        elif self.action in ["list_employee", "create"]:
            permission_classes = [IsEmployeePassport]

        elif self.action == "list_citizen":
            permission_classes = [IsCitizen]

        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    #
    # Perform Create
    #
    def perform_create(self, serializer):

        passport_application_id = self.request.data.get("passport_application")
        passport_application = get_object_or_404(
            PassportApplication, pk=passport_application_id
        )
        departmentx = passport_application.departmentx
        userPass = passport_application.user

        employee = getattr(self.request.user, "employee", None)

        if departmentx == employee.department:
            numbers = "".join(random.choices(string.digits, k=7))
            words = "".join(random.choices(string.ascii_uppercase, k=4))
            passport_number = f"{words}{numbers}"
            #
            # SAVE NEW PASSPORT
            #
            serializer.save(
                status="active",
                user=userPass,
                issuing_authority=departmentx,
                passport_number=passport_number,
            )
        else:
            raise PermissionDenied("You do not have permission to create Passport.")

    #
    # LIST of passports every department
    #
    # - /api/----/list-employee/
    #
    @action(
        detail=False,
        methods=["get"],
        url_path="list-employee",
        url_name="list_employee",
    )
    def list_employee(self, request, *args, **kwargs):

        queryset = self.queryset.filter(
            issuing_authority=request.user.employee.department.id
        ).order_by("-submitted_at")

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    #
    # List for citizens
    #
    @action(
        detail=False,
        methods=["get"],
        url_path="list-citizen",
        url_name="list_citizen",
    )
    def list_citizen(self, request, *args, **kwargs):

        queryset = self.queryset.filter(user=request.user).order_by("-submitted_at")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
