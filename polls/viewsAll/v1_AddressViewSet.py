from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Address, UserAddress
from ..serializers.s1_AddressSerializer import AddressSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from ..permissions.p3_v1_AddressViewPermissions.p1_isAdminOrIsSelfAddress import (
    IsAdminOrIsSelfAddress,
)
from rest_framework.permissions import IsAdminUser


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    format_kwarg = None

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action in ["retrieve", "update", "destroy"]:
            permission_classes = [IsAdminOrIsSelfAddress]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    #
    # Perform create
    #
    def perform_create(self, serializer):
        address = serializer.save()
        user = self.request.user

        UserAddress.objects.create(user=user, address=address)

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
