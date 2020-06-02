from django.shortcuts import render
from . import models
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET", "POST", "PUT", "DELETE"])
def list_rooms(request):
    print(models.Room.objects.all())
    return Response()
