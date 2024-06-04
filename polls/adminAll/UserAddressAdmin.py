from django.contrib import admin
from ..models import UserAddress


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "address")

    search_fields = ("user", "address")

    list_filter = ("user", "address")


admin.site.register(UserAddress, UserAddressAdmin)
