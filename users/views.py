from . import models, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.ReadUserSerializer(request.user).data
        return Response(data=serializer, status=status.HTTP_200_OK)

    def put(self, request, data):
        serializer = serializers.WriteUserSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    def get(self, request, uuid):
        try:
            user = models.User.objects.get(uuid=uuid)
            serializer = serializers.ReadUserSerializer(user).data
            return Response(data=serializer, status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
