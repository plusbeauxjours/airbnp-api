import uuid
from django.db import models
from core.models import CoreModel
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, CoreModel):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    avatar = models.ImageField(upload_to="avatars", blank=True)
    superhost = models.BooleanField(default=False)
    favs = models.ManyToManyField(
        "rooms.Room", related_name="favs", blank=True, null=True
    )

    def room_count(self):
        return self.rooms.count()

    room_count.short_description = "Room Count"

    class Meta:
        ordering = ["-created_at"]
