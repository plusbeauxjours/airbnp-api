from . import models, serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# from rest_framework.generics import ListAPIView, RetrieveAPIView


# class ReadRoomListView(ListAPIView):
#     queryset = models.Room.objects.all()
#     serializer_class = serializers.ReadRoomSerializer


# class ReadRoomDetailView(RetrieveAPIView):
#     queryset = models.Room.objects.all()
#     serializer_class = serializers.ReadRoomSerializer
#     lookup_field = "uuid"


@api_view(["GET", "POST"])
def room_view(request):
    if request.method == "GET":
        rooms = models.Room.objects.all()[:5]
        serializer = serializers.ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = serializers.WriteRoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save(user=request.user)
            room_serializer = serializers.ReadRoomSerializer(room).data
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
