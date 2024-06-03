from django.contrib import admin
from ..models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "employee_type", "department")

    search_fields = (
        "user__username",
        "employee_id",
        "employee_type",
        "department__name",
    )

    list_filter = ("employee_type", "department")

    fieldsets = (
        (None, {"fields": ("user", "employee_id", "employee_type", "department")}),
    )


admin.site.register(Employee, EmployeeAdmin)
