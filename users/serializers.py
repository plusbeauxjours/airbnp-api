from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "uuid",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost",
            "password",
            "room_count",
            "review_count",
        )
        read_only_fields = (
            "uuid",
            "avatar",
            "superhost",
            "room_count",
            "review_count",
        )

    def validate_first_name(self, value):
        return value.upper()

    def validate_last_name(self, value):
        return value.upper()

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class AppleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "uuid",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost",
            "room_count",
            "review_count",
            "apple_id",
        )

    def create(self, validated_data):
        user = super().create(validated_data)
        return user
