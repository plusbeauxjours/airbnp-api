from .models import Room
from .serializers import RoomSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions


class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            # permission_classes = [IsOwner]
            pass
