from django.contrib import admin
from ..models import UserPhoneNumber


class UserPhoneNumberAdmin(admin.ModelAdmin):
    list_display = ("user", "phoneNumber")

    search_fields = ("user", "phoneNumber")

    list_filter = ("user", "phoneNumber")


admin.site.register(UserPhoneNumber, UserPhoneNumberAdmin)
