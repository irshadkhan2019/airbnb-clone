from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "count_rooms",
    )
    filter_horizontal = ("rooms",)
