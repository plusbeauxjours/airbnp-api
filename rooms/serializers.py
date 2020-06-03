from rest_framework import serializers
from users import serializers as user_serializers
from . import models


class RoomListSerializer(serializers.ModelSerializer):
    user = user_serializers.TinyUserSerializer()

    class Meta:
        model = models.Room
        fields = (
            "uuid",
            "name",
            "price",
            "instant_book",
            "user",
        )


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        exclude = ()
