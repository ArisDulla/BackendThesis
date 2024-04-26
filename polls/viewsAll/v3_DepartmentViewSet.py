from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Department
from ..serializers.s3_DepartmentSerializer import DepartmentSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.serializers import ValidationError
from ..processors.addressAndPhone import AddressAndPhoneProcessor


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    format_kwarg = None
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        """
        Create a new Department.
        """
        _processor = AddressAndPhoneProcessor()

        try:
            #
            # CREATE ADDRESS AND PHONE NUMBER
            #
            processed_data = _processor.process_creation_data(request.data)
        except ValidationError as e:
            raise e

        serializer = self.get_serializer(data=processed_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Update an existing Department.
        """
        _processor = AddressAndPhoneProcessor()

        instance = self.get_object()
        try:
            #
            # UPDATE ADDRESS AND PHONE
            #
            _processor.process_update_data(request.data, instance)
        except ValidationError as e:
            raise e

        processed_data = request.data
        #
        #  Remove IDs ADDRESS AND PHONE to exclude from update
        #
        fields_to_exclude = ["address", "phone_number"]
        for field in fields_to_exclude:
            if field in request.data:
                processed_data.pop(field, None)

        serializer = self.get_serializer(instance, data=processed_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
