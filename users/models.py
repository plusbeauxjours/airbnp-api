import uuid
from django.db import models
from rooms.models import Review, Room, Photo
from core.models import CoreModel
from django.contrib.auth.models import AbstractUser

# Seed
import random
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_seed import Seed


class User(AbstractUser, CoreModel):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    avatar = models.ImageField(upload_to="avatars", blank=True)
    superhost = models.BooleanField(default=False)
    favs = models.ManyToManyField("rooms.Room", related_name="favs", blank=True)
    apple_id = models.CharField(blank=True, null=True, max_length=100,)

    def room_count(self):
        return self.rooms.count()

    def review_count(self):
        rooms = self.rooms.all()
        reviews = Review.objects.filter(room__in=rooms)
        return reviews.count()

    room_count.short_description = "Room Count"

    class Meta:
        ordering = ["-created_at"]


# @receiver(post_save, sender=User)
# def do_something_when_user_created(sender, instance, created, **kwargs):
#     if created:
#         user = instance
#         rooms = user.rooms.all()
#         if rooms.count() < 5:
#             room_seeder = Seed.seeder()
#             room_seeder.add_entity(
#                 Room,
#                 3,
#                 {
#                     "uuid": lambda x: uuid.uuid4(),
#                     "user": user,
#                     "name": lambda x: room_seeder.faker.street_address(),
#                     "lat": lambda x: random.uniform(40.706943, 40.822943),
#                     "lng": lambda x: random.uniform(-73.923917, -74.040000),
#                     "price": lambda x: random.randint(60, 300),
#                     "beds": lambda x: random.randint(0, 8),
#                     "bedrooms": lambda x: random.randint(0, 5),
#                     "bathrooms": lambda x: random.randint(0, 5),
#                     "instant_book": lambda x: random.choice([True, False]),
#                     "check_in": lambda x: datetime.now(),
#                     "check_out": lambda x: datetime.now(),
#                 },
#             )
#             room_seeder.execute()

#             review_seeder = Seed.seeder()
#             users = User.objects.all()
#             rooms = user.rooms.all()
#             review_seeder.add_entity(
#                 Review,
#                 20,
#                 {
#                     "uuid": lambda x: uuid.uuid4(),
#                     "user": lambda x: random.choice(users),
#                     "text": lambda x: review_seeder.faker.text(),
#                     "room": lambda x: random.choice(rooms),
#                 },
#             )
#             review_seeder.execute()

#             rooms = user.rooms.all()
#             for room in rooms:
#                 for i in range(random.randint(5, 10)):
#                     Photo.objects.create(
#                         caption=room_seeder.faker.sentence(),
#                         room=room,
#                         file=f"room_photos/{random.randint(1, 50)}.jpeg",
#                     )
