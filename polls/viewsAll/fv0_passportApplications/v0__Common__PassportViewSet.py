from ...permissions.IsStaffOrIsSelf import IsStaffOrIsSelf
from ...permissions.IsStaff_YP01 import IsStaff_YP01
from ...permissions.IsStaff_YP02 import IsStaff_YP02
from ...permissions.IsStaff import IsStaff
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import FileResponse


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
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):

        if self.action == "create":
            permission_classes = [IsAuthenticated]

        elif self.action in [
            "update",
            "cancel_application",
            "retrieve",
            "download_file",
        ]:
            permission_classes = [IsStaffOrIsSelf]

        elif self.action == "first_approval_application":
            permission_classes = [IsStaff_YP01]

        elif self.action == "final_approval_application":
            permission_classes = [IsStaff_YP02]

        elif self.action == "rejected_application":
            permission_classes = [IsStaff]

        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def cancel_application(self, request, pk=None):

        instance = self.get_object()
        instance.status = "cancelated"
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    # Override the update method
    #
    # partial=True
    #
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["post"])
    def first_approval_application(self, request, pk=None):

        instance = self.get_object()
        instance.status = "first_approval"
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["post"])
    def final_approval_application(self, request, pk=None):

        instance = self.get_object()
        instance.status = "final_approval"
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["post"])
    def rejected_application(self, request, pk=None):

        instance = self.get_object()
        instance.status = "rejected"
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    #
    # /api/replacement-passport/24/download-file/FIELD-NAME
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
