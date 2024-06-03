from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from ..models import PhoneNumber
from ..serializers.s2_PhoneNumberSerializer import PhoneNumberSerializer


class PhoneNumberForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        serializer_data = {
            "number": cleaned_data.get("number"),
            "status": cleaned_data.get("status"),
        }

        serializer = PhoneNumberSerializer(data=serializer_data)

        if not serializer.is_valid():

            errors = serializer.errors
            error_message = ", ".join(
                [f"{field}: {', '.join(errors[field])}" for field in errors]
            )
            raise ValidationError(error_message)

        return cleaned_data


class PhoneNumberAdmin(admin.ModelAdmin):
    form = PhoneNumberForm
    list_display = ("number", "status")
    search_fields = ("number",)


admin.site.register(PhoneNumber, PhoneNumberAdmin)
