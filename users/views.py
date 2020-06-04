from .models import User
from rooms.serializers import RoomSerializer
from .serializers import UserSerializer
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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    def get(self, request, uuid):
        try:
            user = User.objects.get(uuid=uuid)
            serializer = UserSerializer(user).data
            return Response(data=serializer, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    def put(self, request):
        pass
