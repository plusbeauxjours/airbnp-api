from . import models, serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class RoomsView(APIView):
    def get(self, request):
        rooms = models.Room.objects.all()[:5]
        serializer = serializers.ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = serializers.WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = serializers.ReadRoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(APIView):
    def get(self, request, uuid):
        try:
            room = models.Room.objects.get(uuid=uuid)
            serializer = serializers.ReadRoomSerializer(room).data
            return Response(data=serializer)
        except models.Room.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        pass

    def delete(self, request):
        pass
