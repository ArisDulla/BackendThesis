from rest_framework import serializers
from ..models import Passport
from django.utils import timezone


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = [
            "last_name",
            "first_name",
            "date_of_birth",
            "place_of_birth",
            "nationality",
            "gender",
            "passport_number",
            "date_of_issue",
            "date_of_expiry",
            "passport_application",
            "status",
        ]
        read_only_fields = ["user", "issuing_authority", "status", "passport_number"]

    def validate_last_name(self, value):
        if not value:
            raise serializers.ValidationError(("Last name is required."))
        return value

    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError(("First name is required."))
        return value

    def validate_date_of_birth(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def validate_date_of_expiry(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError(("Expiry date must be in the future."))
        return value
