from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from ..models import Address
from ..serializers.s1_AddressSerializer import AddressSerializer


class AddressForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        serializer_data = {
            "street": cleaned_data.get("street"),
            "street_number": cleaned_data.get("street_number"),
            "region_name": cleaned_data.get("region_name"),
            "prefecture_name": cleaned_data.get("prefecture_name"),
            "postal_code": cleaned_data.get("postal_code"),
        }

        serializer = AddressSerializer(data=serializer_data)

        if not serializer.is_valid():

            errors = serializer.errors
            error_message = ", ".join(
                [f"{field}: {', '.join(errors[field])}" for field in errors]
            )
            raise ValidationError(error_message)

        return cleaned_data


class AddressAdmin(admin.ModelAdmin):
    form = AddressForm

    list_display = ("__str__",)

    search_fields = (
        "street",
        "street_number",
        "region_name",
        "prefecture_name",
        "postal_code",
    )


admin.site.register(Address, AddressAdmin)
