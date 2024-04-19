from rest_framework import serializers
from ...models import IssuancePassportApplication
from django.core.exceptions import ValidationError


#
# Issuance Passport
#
class IssuancePassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuancePassportApplication
        exclude = ["first_approval_by", "final_approval_by", "user", "rejected_by"]
        read_only_fields = ["status", "user"]

    def validate_application_form(self, value):
        if value:
            if not value.name.endswith(".pdf"):
                raise ValidationError("Only PDF files are allowed for Application form")
            if value.size > 1024 * 1024:  # 1 MB
                raise ValidationError(
                    "Application form pdf file size too large. Max size allowed is 1 MB"
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
