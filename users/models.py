import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    avatar = models.ImageField(upload_to="avatars", blank=True)
    superhost = models.BooleanField(default=False)
    favs = models.ManyToManyField("rooms.Room", related_name="favs")

    def room_count(self):
        return self.rooms.count()

    room_count.short_description = "Room Count"
