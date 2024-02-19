from rest_framework import serializers
from ..models import Department
from ..models import Address
from ..serializers.s1_AddressSerializer import AddressSerializer
from rest_framework.response import Response


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "address", "phone_number", "email"]

        def validate_email(self, value):
            if "@" not in value or "." not in value:
                raise serializers.ValidationError(
                    "Invalid email address. Must contain '@' and '.'"
                )
            return value
