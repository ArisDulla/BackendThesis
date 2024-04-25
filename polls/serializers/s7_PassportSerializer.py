from rest_framework import serializers
from ..models import Passport


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
        ]
        read_only_fields = ["user", "issuing_authority", "status"]
