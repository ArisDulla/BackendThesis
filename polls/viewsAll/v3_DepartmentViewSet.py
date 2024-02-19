from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Department, Address
from ..serializers.s3_DepartmentSerializer import DepartmentSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from ..processors.address import AddressProcessor
from rest_framework.serializers import ValidationError
from ..processors.phoneNumber import PhoneNumberProcessor


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
        #######################################################################
        #
        # Address Data
        #
        address_data = request.data["address"]
        #
        # Create an instance of Address Processor
        #
        address_processor = AddressProcessor()
        #
        # Check if an address with the given data already exists OR create new AND RETURN ID OF ADDRESS
        #
        try:
            address_id = address_processor._verify_unique_address(address_data)
        except ValidationError as e:
            raise e
        #
        # set id here
        #
        request.data["address"] = address_id
        #######################################################################
        #
        # Phone Number Data
        #
        phone_number_data = request.data["phone_number"]
        #
        # Create an instance of Phone Number Processor
        #
        phone_number_processor = PhoneNumberProcessor()
        #
        # Check if an phone number with the given data already exists OR create new AND RETURN ID OF phone number
        #
        try:
            phone_number_id = phone_number_processor._verify_unique_phone_number(
                phone_number_data
            )
        except ValidationError as e:
            raise e
        #
        # set id here
        #
        request.data["phone_number"] = phone_number_id
        
        #print(request.data)
        #######################################################################
        """
        Create a new Department.
        """
        serializer = self.get_serializer(data=request.data)
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
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
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
