import uuid
from django.db import models
from core.models import CoreModel


class Room(CoreModel):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=140)
    address = models.CharField(max_length=140)
    price = models.IntegerField(help_text="USD per night")
    beds = models.IntegerField(default=1)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    check_in = models.TimeField(default="00:00:00")
    check_out = models.TimeField(default="00:00:00")
    instant_book = models.BooleanField(default=False)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="rooms"
    )

    def __str__(self):
        return self.name

    def photo_count(self):
        return self.photos.count()

    def review_count(self):
        return self.reviews.count()

    photo_count.short_description = "Photo Count"
    review_count.short_description = "Review Count"

    class Meta:
        ordering = ["-created_at"]


class Photo(CoreModel):

    file = models.ImageField()
    room = models.ForeignKey(
        "rooms.Room", related_name="photos", on_delete=models.CASCADE
    )
    caption = models.CharField(max_length=140)

    def __str__(self):
        return self.room.name


class Review(CoreModel):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reviews"
    )
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.CharField(max_length=5000)

    def __str__(self):
        return self.room.name
