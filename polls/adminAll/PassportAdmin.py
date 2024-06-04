from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from ..models import Passport
from ..serializers.s7_PassportSerializer import PassportSerializer


class PassportForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        serializer_data = {
            "user": cleaned_data.get("user"),
            "last_name": cleaned_data.get("last_name"),
            "first_name": cleaned_data.get("first_name"),
            "date_of_birth": cleaned_data.get("date_of_birth"),
            "place_of_birth": cleaned_data.get("place_of_birth"),
            "nationality": cleaned_data.get("nationality"),
            "gender": cleaned_data.get("gender"),
            "passport_number": cleaned_data.get("passport_number"),
            "issuing_authority": cleaned_data.get("issuing_authority"),
            "date_of_issue": cleaned_data.get("date_of_issue"),
            "date_of_expiry": cleaned_data.get("date_of_expiry"),
            "status": cleaned_data.get("status"),
            "email_updated_expiry": cleaned_data.get("email_updated_expiry"),
        }

        serializer = PassportSerializer(data=serializer_data)

        if not serializer.is_valid():
            errors = serializer.errors
            error_message = ", ".join(
                [f"{field}: {', '.join(errors[field])}" for field in errors]
            )
            raise ValidationError(error_message)

        return cleaned_data


class PassportAdmin(admin.ModelAdmin):
    form = PassportForm
    list_display = ("passport_number", "last_name", "first_name", "status")
    search_fields = ("passport_number", "last_name", "first_name")
    list_filter = ("status", "nationality", "date_of_expiry")


admin.site.register(Passport, PassportAdmin)
