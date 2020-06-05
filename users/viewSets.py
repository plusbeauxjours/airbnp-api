from .models import User
from .serializers import UserSerializer
from .permissions import IsSelf
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        elif self.action == "create" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsSelf | permissions.IsAdminUser]

        return [permission() for permission in permission_classes]
