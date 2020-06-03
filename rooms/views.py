from django.shortcuts import render
from . import models, serializers
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView


class RoomListView(ListAPIView):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer


class RoomDetailView(RetrieveAPIView):
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
    lookup_field = "uuid"
