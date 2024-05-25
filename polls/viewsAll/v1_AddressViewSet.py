from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Address, UserAddress
from ..serializers.s1_AddressSerializer import AddressSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from ..permissions.p1_AddressPermissions.p1_isAdminOrIsSelfAddress import (
    IsAdminOrIsSelfAddress,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework import status


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    format_kwarg = None

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        elif self.action in ["retrieve", "update", "destroy", "list_user"]:
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
        user_addresses = UserAddress.objects.filter(user=user)
        addresses_data = [
            {
                "id": user_address.address.id,
                "street": user_address.address.street,
                "street_number": user_address.address.street_number,
                "region_name": user_address.address.region_name,
                "prefecture_name": user_address.address.prefecture_name,
                "postal_code": user_address.address.postal_code,
            }
            for user_address in user_addresses
        ]
        return Response(addresses_data, status=status.HTTP_200_OK)
