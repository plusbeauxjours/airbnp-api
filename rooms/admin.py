from django.contrib import admin
from . import models


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "lat",
        "lng",
        "uuid",
        "photo_number",
    )


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "room",
        "text",
    )
