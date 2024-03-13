from rest_framework import viewsets
from ..models import Employee
from ..serializers.s5_EmployeeSerializer import EmployeeSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from ..processors.customUserProcessor import CustomUserProcessor
from rest_framework.serializers import ValidationError
from ..processors.addressAndPhone import AddressAndPhoneProcessor
from ..models import CustomUser


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        """
        Create a new Employee.
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

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        Update an existing Employee.
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
