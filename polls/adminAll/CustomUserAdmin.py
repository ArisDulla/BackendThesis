from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ..models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "is_active",
        "is_admin",
    )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_admin")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_admin",
                ),
            },
        ),
    )

    search_fields = ("email", "username", "first_name", "last_name")

    ordering = ("email",)

    list_filter = ("is_active", "is_admin")


admin.site.register(CustomUser, CustomUserAdmin)
