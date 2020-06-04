from rest_framework import serializers
from . import models


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost",
        )


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        exclude = (
            "groups",
            "user_permissions",
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "is_active",
            "date_joined",
        )


class WriteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("username", "first_name", "last_name", "email")

    def validate_first_name(self, value):
        print(value)
        return value.upper()
