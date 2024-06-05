from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from ..models import IssuancePassportApplication
from ..serializers.fs0_passportApplications.s1_IssuancePassportSerializer import (
    IssuancePassportSerializer,
)
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from PIL import Image
from io import BytesIO
import base64
from django.urls import reverse


class PassportApplicationForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        serializer_data = {
            "user": cleaned_data.get("user"),
            "departmentx": cleaned_data.get("departmentx"),
            "id_card_copy": cleaned_data.get("id_card_copy"),
            "applicant_photo": cleaned_data.get("applicant_photo"),
            "application_form": cleaned_data.get("application_form"),
            "payment_receipt": cleaned_data.get("payment_receipt"),
            "status": cleaned_data.get("status"),
            "first_approval_by": cleaned_data.get("first_approval_by"),
            "final_approval_by": cleaned_data.get("final_approval_by"),
            "rejected_by": cleaned_data.get("rejected_by"),
            "application_type": cleaned_data.get("application_type"),
        }

        serializer = IssuancePassportSerializer(data=serializer_data)

        if not serializer.is_valid():
            errors = serializer.errors
            error_message = ", ".join(
                [f"{field}: {', '.join(errors[field])}" for field in errors]
            )

            raise ValidationError(error_message)

        return cleaned_data


class PassportApplicationAdmin(admin.ModelAdmin):
    form = PassportApplicationForm

    list_display = ("user", "status", "submitted_at")
    search_fields = ("user__username",)
    list_filter = ("status", "submitted_at", "departmentx")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "id_card_copy",
                    "id_card_copy_pdf",
                    "applicant_photo",
                    "applicant_photo_image",
                    "payment_receipt",
                    "payment_receipt_pdf",
                    "application_form",
                    "application_form_pdf",
                    "departmentx",
                    "status",
                    "first_approval_by",
                    "final_approval_by",
                    "rejected_by",
                    "application_type",
                )
            },
        ),
    )
    readonly_fields = (
        "id_card_copy_pdf",
        "applicant_photo_image",
        "payment_receipt_pdf",
        "application_form_pdf",
    )

    def application_form_pdf(self, instance):
        return self.render_file_image(instance, instance.application_form)

    def id_card_copy_pdf(self, instance):
        return self.render_file_image(instance, instance.id_card_copy)

    def applicant_photo_image(self, instance):
        return self.render_file_image(instance, instance.applicant_photo)

    def payment_receipt_pdf(self, instance):
        return self.render_file_image(instance, instance.payment_receipt)

    def render_file_image(self, instance, file_name):

        file_path = str(file_name)
        file_name = file_path.split("/")[-1]
        # print(file_name)
        user = "/".join(file_path.split("/")[:-1])
        # print(file_name)

        if file_name and user:
            download_url = reverse(
                "admin_applabel_modelname_download_file",
                kwargs={"fileName": file_name, "user": user},
            )
            return format_html(
                '<a href="{}" download>{}</a>',
                download_url,
                "-  DOWNLOAD  -  " + file_name,
            )
        else:
            return ""


admin.site.register(IssuancePassportApplication, PassportApplicationAdmin)
