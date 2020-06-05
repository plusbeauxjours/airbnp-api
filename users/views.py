import jwt

from .models import User
from .serializers import UserSerializer
from rooms.models import Room
from rooms.serializers import RoomSerializer

from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserSerializer(user).data
            return Response(data=user_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            serializer = UserSerializer(new_user).data
            return Response(data=serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    def get_user(self, uuid):
        try:
            user = User.objects.get(uuid=uuid)
            return user
        except User.DoesNotExist:
            return None

    def get(self, request, uuid):
        user = self.get_user(uuid)
        if user is not None:
            serializer = UserSerializer(user).data
            return Response(data=serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    def put(self, request):
        uuid = request.data.get("uuid", None)
        user = request.user
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


class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"uuid": str(user.uuid)}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
