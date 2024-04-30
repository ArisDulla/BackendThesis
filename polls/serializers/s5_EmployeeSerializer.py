from rest_framework import serializers
from ..models import Employee
from ..serializers.s4_CustomUserSerializer import CustomUserSerializer
from django.db import transaction


class EmployeeSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Employee
        fields = ["id", "user", "department", "employee_id", "employee_type"]
        read_only_fields = ["employee_id"]

    def create(self, validated_data):

        with transaction.atomic():

            user_data = validated_data.pop("user")

            user_serializer = CustomUserSerializer(data=user_data)
            if user_serializer.is_valid():
                user_instance = user_serializer.save()
            else:
                raise serializers.ValidationError(user_serializer.errors)

            employee_instance = Employee.objects.create(
                user=user_instance, **validated_data
            )
            return employee_instance

    def update(self, instance, validated_data):

        if "user" in validated_data:
            user_data = validated_data.pop("user")
            user_instance = instance.user

            user_serializer = CustomUserSerializer(
                user_instance, data=user_data, partial=True
            )
            if user_serializer.is_valid():
                user_instance = user_serializer.save()
            else:
                raise serializers.ValidationError(user_serializer.errors)

        instance.department = validated_data.get("department", instance.department)
        instance.employee_type = validated_data.get(
            "employee_type", instance.employee_type
        )

        instance.save()

        return instance
