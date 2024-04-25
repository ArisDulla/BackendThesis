from rest_framework import viewsets
from ..models import Cityzens
from ..serializers.s6_CityzensSerializer import CityzensSerializer
from rest_framework.permissions import IsAdminUser
from ..processors.addressAndPhone import AddressAndPhoneProcessor
from rest_framework.serializers import ValidationError
from ..processors.customUserProcessor import CustomUserProcessor
from rest_framework.response import Response
from rest_framework import status
from ..permissions.p1_v0_CommonPassportViewPermissions.p4_isEmployeeOrIsSelf import (
    IsEmployeeOrIsSelf,
)


class CityzensViewSet(viewsets.ModelViewSet):
    queryset = Cityzens.objects.all()
    serializer_class = CityzensSerializer

    def get_permissions(self):
        #
        # The process of creating a citizen is done through the Signal (user_activated) after successful user activation.
        #
        if self.action == "update":
            permission_classes = [IsEmployeeOrIsSelf]

        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    #
    # The function create() is not used because
    #
    # The process of creating a citizen is done through the Signal (user_activated) after successful user activation.
    #
    # NOT USED
    #
    def create(self, request, *args, **kwargs):  # NOT USED
        """
        Create a new Cityzen.
        """
        #
        # Processor DATA Address AND Phone
        #
        _addressAndPhoneProcessor = AddressAndPhoneProcessor()
        try:
            custom_user_data = _addressAndPhoneProcessor.process_creation_data(
                request.data["user"]
            )
        except ValidationError as e:
            raise e

        #
        # Processor DATA Custom User
        #
        _customUserProcessor = CustomUserProcessor()

        try:
            user_array = _customUserProcessor._create_custom_user(custom_user_data)
        except ValidationError as e:
            raise e

        request.data["user"] = user_array["user_id"]

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        except Exception as e:
            user_array["instance"].delete()

        return Response(
            {"data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        Update an existing Cityzen.
        """

        instance = self.get_object()
        user_id = instance.user_id

        if "user" in request.data:

            #
            # Processor DATA Address AND Phone
            #
            _addressAndPhoneProcessor = AddressAndPhoneProcessor()
            try:
                custom_user_data = _addressAndPhoneProcessor.process_creation_data(
                    request.data["user"]
                )
            except ValidationError as e:
                raise e

            #
            # Processor DATA Custom User
            #
            _customUserProcessor = CustomUserProcessor()
            existing_custom_user = instance.user

            try:
                _customUserProcessor._update_custom_user(
                    existing_custom_user, custom_user_data
                )
            except ValidationError as e:
                raise e

            request.data["user"] = user_id

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
