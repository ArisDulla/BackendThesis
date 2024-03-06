from rest_framework import viewsets
from ..models import Cityzens
from ..serializers.s6_CityzensSerializer import CityzensSerializer
from rest_framework.permissions import IsAdminUser
from ..processors.addressAndPhone import AddressAndPhoneProcessor
from rest_framework.serializers import ValidationError
from ..processors.customUserProcessor import CustomUserProcessor
from rest_framework.response import Response
from rest_framework import status


class CityzensViewSet(viewsets.ModelViewSet):
    queryset = Cityzens.objects.all()
    serializer_class = CityzensSerializer

    def create(self, request, *args, **kwargs):
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
            user_id = _customUserProcessor._create_custom_user(custom_user_data)
        except ValidationError as e:
            raise e

        request.data["user"] = user_id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
