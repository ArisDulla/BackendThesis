from ...permissions.p0_CommonPassportPermissions.p4_isEmployeeOrIsSelf import (
    IsEmployeeOrIsSelf,
)
from ...permissions.p0_CommonPassportPermissions.p0_isEmployee_YP01 import (
    IsEmployee_YP01,
)
from ...permissions.p0_CommonPassportPermissions.p1_isEmployee_YP02 import (
    IsEmployee_YP02,
)
from ...permissions.p0_CommonPassportPermissions.p3_isEmployeeObject import (
    IsEmployeeObject,
)
from ...permissions.p0_CommonPassportPermissions.p2_isEmployee import isEmployee
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import FileResponse
from ...permissions.p1_isCitizen import IsCitizen
from ...serializers.fs0_passportApplications.s0_PassportApplicationSerializer import (
    PassportApplicationSerializer,
)
from ...models import PassportApplication


#
# Abstract base class for common behavior of viewsets
#
# + IssuancePassportViewSet
# + RenewalPassportViewSet
# + ReplacementPassportViewSet
# + TheftOrLossPassportViewSet
# + IssuanceMinorsPassportViewSet
#
class CommonPassportViewSet(viewsets.ModelViewSet):
    queryset = PassportApplication.objects.all()
    serializer_class = PassportApplicationSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):

        if self.action == "create":
            permission_classes = [IsAuthenticated]

        elif self.action == "list_citizen":
            permission_classes = [IsCitizen]

        elif self.action in [
            "update",
            "cancel_application",
            "retrieve",
            "download_file",
        ]:
            permission_classes = [IsEmployeeOrIsSelf]

        elif self.action in [
            "list_employee",
            "list_employee_offield",
        ]:

            permission_classes = [isEmployee]

        elif self.action == "first_approval_application":
            permission_classes = [IsEmployee_YP01]

        elif self.action == "final_approval_application":
            permission_classes = [IsEmployee_YP02]

        elif self.action == "rejected_application":
            permission_classes = [IsEmployeeObject]

        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    #
    # CREATE
    #
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    #
    # Cancel Application
    #
    @action(detail=True, methods=["post"])
    def cancel_application(self, request, pk=None):

        instance = self.get_object()
        instance.status = "cancelated"
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

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
    # First Approval Application
    #
    @action(detail=True, methods=["post"])
    def first_approval_application(self, request, pk=None):

        instance = self.get_object()
        instance.status = "first_approval"
        instance.first_approval_by = request.user
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    #
    # Final Approval Application
    #
    @action(detail=True, methods=["post"])
    def final_approval_application(self, request, pk=None):

        instance = self.get_object()
        instance.status = "final_approval"
        instance.final_approval_by = request.user
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    #
    # Rejected Application
    #
    @action(detail=True, methods=["post"])
    def rejected_application(self, request, pk=None):

        instance = self.get_object()
        instance.status = "rejected"
        instance.rejected_by = request.user
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    #
    #
    # Download File
    #
    # /api/--------/24/download-file/FIELD-NAME
    #
    @action(
        detail=True,
        methods=["get"],
        url_name="download-file",
        url_path=r"download-file/(?P<nameoffield>\w+)",
    )
    def download_file(self, request, pk=None, nameoffield=None):

        try:
            instance = self.get_object()
            file_field = getattr(instance, nameoffield)
        except AttributeError:
            return JsonResponse({"error": "File field not found"}, status=404)

        if not file_field:
            return JsonResponse({"error": "File field not found"}, status=404)

        file_path = file_field.path
        try:

            return FileResponse(open(file_path, "rb"), as_attachment=True)
        except FileNotFoundError:
            return JsonResponse({"error": "File field not found"}, status=404)

    #
    # LIST of applications every department
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
            departmentx=request.user.employee.department.id
        ).order_by("-submitted_at")

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    #
    # LIST of applications status = FIELD-NAME
    #
    # - /api/----/list-employee-offield/FIELD-NAME
    #
    @action(
        detail=False,
        methods=["get"],
        url_name="list-employee-offield",
        url_path=r"list-employee-offield/(?P<nameoffield>\w+)",
    )
    def list_employee_offield(self, request, pk=None, nameoffield=None):

        queryset = self.queryset.filter(
            departmentx=request.user.employee.department.id, status=nameoffield
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
