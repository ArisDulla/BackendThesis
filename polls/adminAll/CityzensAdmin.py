from django.contrib import admin
from ..models import Cityzens


class CitizensAdmin(admin.ModelAdmin):
    list_display = ("user", "department")
    search_fields = ("user__username", "department__name")
    fieldsets = ((None, {"fields": ("user", "department")}),)


admin.site.register(Cityzens, CitizensAdmin)
