from django.contrib import admin
from core.models import (
    Person,
)


class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "dni", "sex")
    ordering = ["name"]


admin.site.register(Person, PersonAdmin)
