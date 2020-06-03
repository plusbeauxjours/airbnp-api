from django.contrib import admin
from . import models


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "uuid",
        "photo_number",
    )


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
