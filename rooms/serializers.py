from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Room, Photo, Review


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = ("room",)


class RoomSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    photos = PhotoSerializer(read_only=True, many=True)
    is_fav = serializers.SerializerMethodField()

    class Meta:
        model = Room
        exclude = ("updated_at",)
        read_only_fields = ("user", "id", "uuid", "created_at", "updated_at")

    def validate(self, data):
        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
        if check_in == check_out:
            raise serializers.ValidationError("Not enough time between changes")
        return data

    def get_is_fav(self, obj):
        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return False

    def create(self, validated_data):
        request = self.context.get("request")
        room = Room.objects.create(**validated_data, user=request.user)
        return room


class ReviewSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        exclude = ("updated_at",)
        read_only_fields = ("user", "text", "id", "uuid", "created_at", "updated_at")

    def create(self, validated_data):
        request = self.context.get("request")
        review = Review.objects.create(**validated_data, user=request.user)
        return review
