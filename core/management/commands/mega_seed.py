import uuid
import random
from datetime import datetime
from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User
from rooms.models import Room, Photo, Review


class Command(BaseCommand):

    help = "It seeds the DB with tons of stuff"

    def handle(self, *args, **options):
        rooms = Room.objects.all()
        rooms.delete()
        user_seeder = Seed.seeder()
        user_seeder.add_entity(
            User,
            20,
            {
                "uuid": lambda x: uuid.uuid4(),
                "avatar": None,
                "is_staff": False,
                "is_superuser": False,
            },
        )
        user_seeder.execute()

        users = User.objects.all()
        room_seeder = Seed.seeder()
        room_seeder.add_entity(
            Room,
            600,
            {
                "uuid": lambda x: uuid.uuid4(),
                "user": lambda x: random.choice(users),
                "name": lambda x: room_seeder.faker.street_address(),
                "lat": lambda x: random.uniform(40.706943, 40.822943),
                "lng": lambda x: random.uniform(-73.923917, -74.040000),
                "price": lambda x: random.randint(60, 300),
                "beds": lambda x: random.randint(0, 8),
                "bedrooms": lambda x: random.randint(0, 5),
                "bathrooms": lambda x: random.randint(0, 5),
                "instant_book": lambda x: random.choice([True, False]),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now(),
            },
        )
        room_seeder.execute()

        rooms = Room.objects.all()
        for room in rooms:
            for i in range(random.randint(5, 10)):
                Photo.objects.create(
                    caption=room_seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.jpeg",
                )

        users = User.objects.all()
        rooms = Room.objects.all()
        review_seeder = Seed.seeder()
        review_seeder.add_entity(
            Review,
            600,
            {
                "uuid": lambda x: uuid.uuid4(),
                "user": lambda x: random.choice(users),
                "text": lambda x: review_seeder.faker.text(),
                "room": lambda x: random.choice(rooms),
            },
        )
        room_seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"Everything seeded"))
