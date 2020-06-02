from rest_framework import serializers
from users import serializers as user_serializers
from . import models


class RoomSerializer(serializers.ModelSerializer):
    user = user_serializers.TinyUserSerializer()

    class Meta:
        model = models.Room
        fields = ("name", "price", "instant_book", "user")
