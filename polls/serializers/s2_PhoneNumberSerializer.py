from rest_framework import serializers
from ..models import PhoneNumber


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ["id", "number", "status"]
        read_only_fields = ["status"]

    def validate_number(self, value):
        """
        Check that the phone number has exactly 10 digits and contains only numeric characters.
        """
        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only numeric digits."
            )
        if len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must have exactly 10 digits."
            )
        return value
