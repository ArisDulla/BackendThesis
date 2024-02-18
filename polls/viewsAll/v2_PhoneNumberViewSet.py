from rest_framework import viewsets
from rest_framework.response import Response
from ..models import PhoneNumber
from ..serializers.s2_PhoneNumberSerializer import PhoneNumberSerializer
from rest_framework import status
from rest_framework.permissions import IsAdminUser


class PhoneNumberViewSet(viewsets.ModelViewSet):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer
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
        Return a list of all PhoneNumbers.
        """

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new PhoneNumber.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single PhoneNumber instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update an existing PhoneNumber.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing PhoneNumber.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
