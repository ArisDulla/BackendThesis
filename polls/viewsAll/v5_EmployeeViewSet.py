from rest_framework import viewsets
from ..models import Employee
from ..serializers.s5_EmployeeSerializer import EmployeeSerializer
from rest_framework.permissions import IsAdminUser
import random
import string
from rest_framework.response import Response


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):

        numbers = "".join(random.choices(string.digits, k=7))
        words = "".join(random.choices(string.ascii_uppercase, k=5))
        employee_id = f"{words}{numbers}"

        serializer.save(employee_id=employee_id)

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
