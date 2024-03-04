from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Department, Address
from ..serializers.s3_DepartmentSerializer import DepartmentSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from ..processors.addressProcessor import AddressProcessor
from rest_framework.serializers import ValidationError
from ..processors.addressAndPhone import DepartmentCreationProcessor


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    format_kwarg = None
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        """
        Create a new Department.
        """
        processor = DepartmentCreationProcessor()

        try:
            processed_data = processor.process_creation_data(request.data)
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
        processor = DepartmentCreationProcessor()

        try:
            processed_data = processor.process_creation_data(request.data)
        except ValidationError as e:
            raise e

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=processed_data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
