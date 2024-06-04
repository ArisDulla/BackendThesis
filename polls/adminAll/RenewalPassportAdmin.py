from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from ..models import RenewalPassportApplication
from ..serializers.fs0_passportApplications.s2_RenewalPassportSerializer import (
    RenewalPassportSerializer,
)
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from PIL import Image
from io import BytesIO
import base64
from django.urls import reverse


class RenewalPassportForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        serializer_data = {
            "user": cleaned_data.get("user"),
            "departmentx": cleaned_data.get("departmentx"),
            "id_card_copy": cleaned_data.get("id_card_copy"),
            "applicant_photo": cleaned_data.get("applicant_photo"),
            "old_passport_pdf": cleaned_data.get("old_passport_pdf"),
            "payment_receipt": cleaned_data.get("payment_receipt"),
            "status": cleaned_data.get("status"),
            "first_approval_by": cleaned_data.get("first_approval_by"),
            "final_approval_by": cleaned_data.get("final_approval_by"),
            "rejected_by": cleaned_data.get("rejected_by"),
            "application_type": cleaned_data.get("application_type"),
        }

        serializer = RenewalPassportSerializer(data=serializer_data)

        if not serializer.is_valid():
            errors = serializer.errors
            error_message = ", ".join(
                [f"{field}: {', '.join(errors[field])}" for field in errors]
            )

            raise ValidationError(error_message)

        return cleaned_data


class RenewalPassportAdmin(admin.ModelAdmin):
    form = RenewalPassportForm

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
                    "applicant_photo_image_display",
                    "applicant_photo",
                    "applicant_photo_image",
                    "payment_receipt",
                    "payment_receipt_pdf",
                    "old_passport_pdf",
                    "old_passport_pdf_pdf",
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
        "applicant_photo_image_display",
        "id_card_copy_pdf",
        "applicant_photo_image",
        "payment_receipt_pdf",
        "old_passport_pdf_pdf",
    )

    def applicant_photo_image_display(self, instance):
        return self.render_applicant_photo(instance.applicant_photo)

    def old_passport_pdf_pdf(self, instance):
        return self.render_file_image(instance, instance.old_passport_pdf)

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

    def render_applicant_photo(self, file_field):
        if file_field:
            img = Image.open(file_field)
            img.thumbnail((200, 200))
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return mark_safe(f'<img src="data:image/jpeg;base64,{img_str}" />')
        else:
            return "No Image"


admin.site.register(RenewalPassportApplication, RenewalPassportAdmin)
