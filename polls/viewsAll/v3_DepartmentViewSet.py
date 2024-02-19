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

    def initial(self, request, *args, **kwargs):
        """
        Perform any necessary initializations.
        """
        # Your initialization logic here
        pass

    def list(self, request, *args, **kwargs):
        """
        Return a list of all Department.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single Department instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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

    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing Department.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
