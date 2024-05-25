from rest_framework import serializers
from ...models import IssuanceMinorsPassportApplication
from django.core.exceptions import ValidationError


#
# Issuance Minors Passport
#
#
class IssuanceMinorsPassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuanceMinorsPassportApplication
        exclude = [
            "first_approval_by",
            "final_approval_by",
            "user",
            "rejected_by",
            "departmentx",
        ]
        read_only_fields = ["status", "user", "departmentx"]

    def validate_minor_age_declaration(self, value):
        if value:
            if not value.name.endswith(".pdf"):
                raise ValidationError(
                    "Only PDF files are allowed for minor age declaration"
                )
            if value.size > 1024 * 1024:  # 1 MB
                raise ValidationError(
                    "Minor age declaration file size too large. Max size allowed is 1 MB"
                )
        return value

    def validate_convicted_declaration(self, value):
        if value:
            if not value.name.endswith(".pdf"):
                raise ValidationError(
                    "Only PDF files are allowed for convicted declaration"
                )
            if value.size > 1024 * 1024:  # 1 MB
                raise ValidationError(
                    "Convicted declaration file size too large. Max size allowed is 1 MB"
                )
        return value

    def validate_caregiver_address_certification(self, value):
        if value:
            if not value.name.endswith(".pdf"):
                raise ValidationError(
                    "Only PDF files are allowed for caregiver address certification"
                )
            if value.size > 1024 * 1024:  # 1 MB
                raise ValidationError(
                    "Caregiver address certification file size too large. Max size allowed is 1 MB"
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
