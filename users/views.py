from . import models, serializers
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class MeView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            serializer = serializers.ReadUserSerializer(request.user).data
            return Response(data=serializer, status=status.HTTP_200_OK)

    def put(self, request, data):
        return data


@api_view(["GET"])
def user_detail(request, uuid):
    try:
        user = models.User.objects.get(uuid=uuid)
        serializer = serializers.ReadUserSerializer(user).data
        return Response(data=serializer, status=status.HTTP_200_OK)
    except models.User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
