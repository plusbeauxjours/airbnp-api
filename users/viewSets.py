import jwt

from .models import User
from rooms.models import Room, Review
from rooms.serializers import RoomSerializer, ReviewSerializer
from .serializers import UserSerializer, AppleSerializer
from .permissions import IsSelf

from django.conf import settings
from django.contrib.auth import authenticate

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
        elif (
            self.action == "create"
            or self.action == "retrieve"
            or self.action == "favs"
            or self.action == "toggle_favs"
            or self.action == "reviews"
            or self.action == "rooms"
            or self.action == "appleLogin"
        ):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsSelf]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"uuid": str(user.uuid)}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "uuid": str(user.uuid)})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True)
    def favs(self, request, uuid):
        user = self.get_object()
        serializer = RoomSerializer(
            user.favs.all(), many=True, context={"request": request}
        ).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    @favs.mapping.put
    def toggle_favs(self, request, uuid):
        uuid = request.data.get("uuid", None)
        user = self.get_object()
        if uuid is not None:
            try:
                room = Room.objects.get(uuid=uuid)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                serializer = RoomSerializer(user.favs.all(), many=True).data
                return Response(data=serializer, status=status.HTTP_200_OK)
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def reviews(self, request, uuid):
        user = self.get_object()
        if user:
            try:
                rooms = user.rooms.all()
                reviews = Review.objects.filter(room__in=rooms)
                serializer = ReviewSerializer(reviews, many=True).data
                return Response(data=serializer, status=status.HTTP_200_OK)
            except Review.DoesNotExist:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True)
    def rooms(self, request, uuid):
        user = self.get_object()
        serializer = RoomSerializer(
            user.rooms.all(), many=True, context={"request": request}
        ).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def appleLogin(self, request):
        apple_id = request.data.get("apple_id", None)
        print(apple_id)
        try:
            user = User.objects.get(apple_id=apple_id)
            encoded_jwt = jwt.encode(
                {"uuid": str(user.uuid)}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(
                data={"token": encoded_jwt, "uuid": str(user.uuid)},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            serializer = AppleSerializer(data=request.data)
            if serializer.is_valid():
                new_user = serializer.save()
                encoded_jwt = jwt.encode(
                    {"uuid": str(new_user.uuid)}, settings.SECRET_KEY, algorithm="HS256"
                )
                return Response(
                    data={"token": encoded_jwt, "uuid": str(new_user.uuid)},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
