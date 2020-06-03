from django.shortcuts import render
from . import models, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response


# @api_view(["GET"])
# def room_list(request):
#     rooms = models.Room.objects.all()
#     serialized_rooms = serializers.RoomListSerializer(rooms, many=True)
#     return Response(serialized_rooms.data)

# from rest_framework.views import APIView


# class RoomListView(APIView):
#     def get(self, request):
#         rooms = models.Room.objects.all()
#         serializer = serializers.RoomListSerializer(rooms, many=True)
#         return Response(serializer.data)

from rest_framework.generics import ListAPIView


class RoomListView(ListAPIView):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomListSerializer


from rest_framework.generics import RetrieveAPIView


class RoomDetailView(RetrieveAPIView):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomDetailSerializer
    lookup_field = "uuid"
