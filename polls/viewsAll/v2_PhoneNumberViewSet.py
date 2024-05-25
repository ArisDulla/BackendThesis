from rest_framework import viewsets
from rest_framework.response import Response
from ..models import PhoneNumber, UserPhoneNumber
from ..serializers.s2_PhoneNumberSerializer import PhoneNumberSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from ..permissions.p2_PhoneNumberPermissions.p1_isAdminOrIsSelfPhoneNumber import (
    IsAdminOrIsSelfNumber,
)
from rest_framework.decorators import action
from rest_framework import status


class PhoneNumberViewSet(viewsets.ModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer
    format_kwarg = None

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]

        elif self.action in ["retrieve", "update", "destroy", "list_user"]:
            permission_classes = [IsAdminOrIsSelfNumber]

        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    #
    # Perform create
    #
    def perform_create(self, serializer):
        phoneNumber = serializer.save()
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
        user_phone_numbers = UserPhoneNumber.objects.filter(user=user)
        phone_numbers_data = [
            {
                "id": user_phone_number.phoneNumber.id,
                "number": user_phone_number.phoneNumber.number,
            }
            for user_phone_number in user_phone_numbers
        ]
        return Response(phone_numbers_data, status=status.HTTP_200_OK)
