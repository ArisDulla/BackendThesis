from rest_framework import viewsets
from ..models import Employee
from ..serializers.s5_EmployeeSerializer import EmployeeSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from ..processors.customUserProcessor import CustomUserProcessor
from rest_framework.serializers import ValidationError
import random
import string


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):

        numbers = "".join(random.choices(string.digits, k=7))
        words = "".join(random.choices(string.ascii_uppercase, k=5))
        employee_id = f"{words}{numbers}"

        serializer.save(employee_id=employee_id)

    def create(self, request, *args, **kwargs):
        """
        Create a new Employee.
        """

        custom_user_data = request.data["user"]
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
            raise e

        return Response(
            {"data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        Update an existing Employee.
        """
        instance = self.get_object()

        if "user" in request.data:

            user_id = instance.user.id

            custom_user_data = request.data["user"]
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

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
