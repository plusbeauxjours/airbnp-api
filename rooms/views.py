from . import models, serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class RoomsView(APIView):
    def get(self, request):
        rooms = models.Room.objects.all()[:5]
        serializer = serializers.ReadRoomSerializer(rooms, many=True).data
        return Response(data=serializer)

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
    def get_room(self, uuid):
        try:
            room = models.Room.objects.get(uuid=uuid)
            return room
        except models.Room.DoesNotExist:
            return None

    def get(self, request, uuid):
        print(uuid)
        room = self.get_room(uuid)
        if room is not None:
            serializer = serializers.ReadRoomSerializer(room).data
            return Response(data=serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uuid):
        room = self.get_room(uuid)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = serializers.WriteRoomSerializer(
                room, data=request.data, partial=True
            )
            if serializer.is_valid():
                room = serializer.save()
                room_serializer = serializers.ReadRoomSerializer(room).data
                return Response(data=room_serializer, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        room = self.get_room(uuid)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
