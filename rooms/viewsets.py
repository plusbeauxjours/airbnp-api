from rest_framework import viewsets
from . import models
from . import serializers


class RoomViewset(viewsets.ModelViewSet):

    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomDetailSerializer
    lookup_field = "uuid"
