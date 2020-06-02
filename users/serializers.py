from rest_framework import serializers
from . import models


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("username", "superhost")
