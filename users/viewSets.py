from .models import User
from .serializers import UserSerializer
from .permissions import IsSelf
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        elif self.action == "create" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsSelf | permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

    @action(detail=False)
    def me(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request.user).data
        return Response(data=serializer, status=status.HTTP_200_OK)
