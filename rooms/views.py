from django.shortcuts import render
from . import models, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


# @api_view(["GET"])
# def list_rooms(request):
#     rooms = models.Room.objects.all()
#     serialized_rooms = serializers.RoomSerializer(rooms, many=True)
#     return Response(serialized_rooms.data)

from rest_framework.views import APIView


# class ListRoomsView(APIView):
#     def get(self, request):
#         rooms = models.Room.objects.all()
#         serializer = serializers.RoomSerializer(rooms, many=True)
#         return Response(serializer.data)

from rest_framework.generics import ListAPIView


class ListRoomsView(ListAPIView):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
