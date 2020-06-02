from django.shortcuts import render
from . import models
from . import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def list_rooms(request):
    rooms = models.Room.objects.all()
    serialized_rooms = serializers.RoomSerializer(rooms, many=True)
    return Response(data=serialized_rooms.data)
