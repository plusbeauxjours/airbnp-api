from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class UserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Profile", {"fields": ("avatar", "superhost", "favs", "apple_id")},),
    )

    list_display = UserAdmin.list_display + ("room_count", "review_count", "uuid",)
