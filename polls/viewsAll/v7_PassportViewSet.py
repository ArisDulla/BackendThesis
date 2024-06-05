from rest_framework import viewsets
from ..models import Passport
from ..serializers.s7_PassportSerializer import PassportSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from ..permissions.p7_PassportPermissions.p1_isEmployeeObjectPassport import (
    IsEmployeeObjectPassport,
)
from ..permissions.p7_PassportPermissions.p2_isEmployeeOrIsSelfPassport import (
    IsEmployeeOrIsSelfPassport,
)
from ..permissions.p7_PassportPermissions.p3_isEmployeePassport import (
    IsEmployeePassport,
)
from ..permissions.p7_PassportPermissions.p4_IsEmployeeYp2 import (
    IsEmployeeYP2,
)
from django.shortcuts import get_object_or_404
from polls.models import PassportApplication
from ..permissions.p1_isCitizen import IsCitizen
import random
import string
from rest_framework.exceptions import ValidationError
from rest_framework import status


class PassportViewSet(viewsets.ModelViewSet):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer

    def get_permissions(self):

        if self.action == "update":
            permission_classes = [IsEmployeeObjectPassport]

        elif self.action in ["retrieve", "get_passport"]:
            permission_classes = [IsEmployeeOrIsSelfPassport]

        elif self.action in ["list_employee"]:
            permission_classes = [IsEmployeePassport]

        elif self.action == "create":
            permission_classes = [IsEmployeeYP2]

        elif self.action == "list_citizen":
            permission_classes = [IsCitizen]

        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    #
    # Create
    #
    def _get_passport_application(self):
        passport_application_id = self.request.data.get("passport_application")
        return get_object_or_404(PassportApplication, pk=passport_application_id)

    def create(self, request, *args, **kwargs):
        passport_application = self._get_passport_application()
        departmentx = passport_application.departmentx

        employee = getattr(self.request.user, "employee", None)

        if passport_application.status != "final_approval":
            raise ValidationError(
                {
                    "Notify": [
                        "You can only perform this action when the status is 'final_approval'."
                    ]
                }
            )

        if departmentx != employee.department:

            raise ValidationError(
                {
                    "Notify": [
                        "The citizen's department does not match the employee's department."
                    ]
                }
            )

        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            errors = serializer.errors
            #
            # when already exists passport (( OneToOneField ))
            #
            if "passport_application" in errors:
                return Response(
                    {"passport_application": errors["passport_application"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):

        passport_application = self._get_passport_application()
        departmentx = passport_application.departmentx
        userPass = passport_application.user

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

    #
    # Get Passport
    #
    @action(
        detail=False,
        methods=["get"],
        url_name="get-passport",
        url_path=r"get-passport/(?P<idApplication>\w+)",
    )
    def get_passport(self, request, pk=None, idApplication=None):

        try:
            passport = Passport.objects.get(passport_application=idApplication)
            serializer = PassportSerializer(passport)
            return Response(serializer.data)
        except Passport.DoesNotExist:
            return Response({"error": "Passport not found"}, status=404)
