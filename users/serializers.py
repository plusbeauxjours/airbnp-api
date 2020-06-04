from rest_framework import serializers
from .models import User


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "superhost",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = (
            "id",
            "uuid",
            "groups",
            "user_permissions",
            "password",
            "is_superuser",
            "is_staff",
            "is_active",
            "favs",
            "last_login",
            "date_joined",
        )

    def validate_first_name(self, value):
        print(value)
        return value.upper()
