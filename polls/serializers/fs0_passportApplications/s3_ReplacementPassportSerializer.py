from rest_framework import serializers
from ...models import ReplacementPassportApplication
from django.core.exceptions import ValidationError


#
# Replacement Passport
#
#
class ReplacementPassportSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = ReplacementPassportApplication
        exclude = [
            "first_approval_by",
            "final_approval_by",
            "user",
            "rejected_by",
            "departmentx",
        ]
        read_only_fields = ["status", "user", "departmentx"]

    def get_user_details(self, obj):

        user = obj.user

        return {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

    def validate_old_passport_pdf(self, value):
        if value:
            if not value.name.endswith(".pdf"):
                raise ValidationError("Only PDF files are allowed for old passport")
            if value.size > 1024 * 1024:  # 1 MB
                raise ValidationError(
                    "Old passport file size too large. Max size allowed is 1 MB"
                )
        return value

    def validate_id_card_copy(self, value):
        if value:
            if not value.name.endswith(".pdf"):
                raise ValidationError("Only PDF files are allowed for id card copy")
            if value.size > 1024 * 1024:  # 1 MB
                raise ValidationError(
                    "Id card copy file size too large. Max size allowed is 1 MB"
                )
        return value

    def validate_payment_receipt(self, value):
        if value:
            if not value.name.endswith(".pdf"):
                raise ValidationError("Only PDF files are allowed for payment receipt")
            if value.size > 1024 * 1024:  # 1 MB
                raise ValidationError(
                    "Payment receipt file size too large. Max size allowed is 1 MB"
                )
        return value

    def validate_applicant_photo(self, value):

        # Check if the file size is greater than 1 MB (1048576 bytes)
        max_size = 1048576  # 1 MB
        if value.size > max_size:
            raise ValidationError(("The maximum file size allowed is 1 MB."))

        return value
