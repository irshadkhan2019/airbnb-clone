from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin Definition"""

    list_display = (
        "name",
        "used_by",
    )

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img width="100px"src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    inlines = (PhotoInline,)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "address",
                    "price",
                )
            },
        ),
        (
            "Times",
            {
                "fields": (
                    "check_in",
                    "check_out",
                    "instant_book",
                )
            },
        ),
        (
            "Spaces",
            {
                "fields": (
                    "beds",
                    "bedrooms",
                    "baths",
                    "guests",
                )
            },
        ),
        (
            "More About Space",
            {
                "classes": ("collapse",),
                "fields": (
                    "amenities",
                    "facilities",
                    "house_all_rules",
                ),
            },
        ),
        (
            "Last Details",
            {"fields": ("host", "room_type")},
        ),
    )

    list_display = (
        "name",
        "description",
        "city",
        "price",
        "beds",
        "bedrooms",
        "baths",
        "guests",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )
    list_filter = (
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_all_rules",
        "host__superhost",
        "city",
        "country",
    )
    search_fields = ("=city", "^host__username")

    ordering = ("name", "price")

    raw_id_fields = ("host",)

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_all_rules",
    )

    # Intercept dave from admin panel
    def save_model(self, request, obj, form, change):
        return super().save_model(request, obj, form, change)

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()
