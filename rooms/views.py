from .models import Room
from .serializers import RoomSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class OwnPagination(PageNumberPagination):
    page_size = 5


class RoomSearchView(APIView):
    def get(self, request):
        paginator = OwnPagination()
        rooms = Room.objects.filter()
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)


class RoomsView(APIView):
    def get(self, request):
        paginator = OwnPagination()
        rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(results, many=True).data
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = RoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(APIView):
    def get_room(self, uuid):
        try:
            room = Room.objects.get(uuid=uuid)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, uuid):
        room = self.get_room(uuid)
        if room is not None:
            serializer = RoomSerializer(room).data
            return Response(data=serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, uuid):
        room = self.get_room(uuid)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = RoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                room = serializer.save()
                room_serializer = RoomSerializer(room).data
                return Response(data=room_serializer, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
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
