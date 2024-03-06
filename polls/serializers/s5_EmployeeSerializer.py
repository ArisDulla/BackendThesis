from rest_framework import serializers
from ..models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "user", "department", "employee_id", "employee_type"]
