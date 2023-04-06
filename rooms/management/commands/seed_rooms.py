import random
from django.contrib.admin.utils import flatten
from django.core.management.base import BaseCommand
from django_seeder import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command creates Rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many Rooms you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "guests": lambda x: random.randint(1, 10),
                "price": lambda x: random.randint(1, 300),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        created_rooms = seeder.execute()  # returns pk's of created rooms

        # Create photos for rooms
        created_clean_rooms = flatten(list(created_rooms.values()))

        for room in created_clean_rooms:
            room = room_models.Room.objects.get(pk=room)

            for photo in range(3, random.randint(6, 12)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"/room_photos/{random.randint(1,10)}.jpg",
                )
            # Create amenties for rooms
            for amenity in amenities:
                magic_number = random.randint(0, 5)
                if magic_number % 2 == 0:
                    room.amenities.add(amenity)

            # Create amenties for rooms
            for facility in facilities:
                magic_number = random.randint(0, 5)
                if magic_number % 2 == 0:
                    room.facilities.add(facility)

            # Create rules for rooms
            for rule in rules:
                magic_number = random.randint(0, 5)
                if magic_number % 2 == 0:
                    room.house_all_rules.add(rule)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created :)"))
