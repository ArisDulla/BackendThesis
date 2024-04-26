from rest_framework import viewsets
from rest_framework.response import Response
from ..models import PhoneNumber, UserPhoneNumber
from ..serializers.s2_PhoneNumberSerializer import PhoneNumberSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from ..permissions.p4_v2_PhoneNumberViewPermissions.p1_isAdminOrIsSelfPhoneNumber import (
    IsAdminOrIsSelfNumber,
)


class PhoneNumberViewSet(viewsets.ModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer
    format_kwarg = None

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]

        elif self.action in ["retrieve", "update", "destroy"]:
            permission_classes = [IsAdminOrIsSelfNumber]

        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    #
    # Perform create
    #
    def perform_create(self, serializer):
        phoneNumber = serializer.save(status="active")
        user = self.request.user

        UserPhoneNumber.objects.create(user=user, phoneNumber=phoneNumber)

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
