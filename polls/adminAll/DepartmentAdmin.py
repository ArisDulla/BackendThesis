from django.contrib import admin
from ..models import Department


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone_number", "email")

    search_fields = ("name", "address__address_line", "phone_number__number", "email")

    list_filter = ("address", "phone_number")


admin.site.register(Department, DepartmentAdmin)
