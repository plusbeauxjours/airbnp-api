from .models import Room, Review
from .permissions import IsOwner
from .serializers import RoomSerializer, ReviewSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, status


class RoomViewSet(ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"

    def get_permissions(self):
        if (
            self.action == "list"
            or self.action == "retrieve"
            or self.action == "reviews"
        ):
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def search(self, request):
        search = request.GET.get("search", None)
        max_price = request.GET.get("max_price", None)
        min_price = request.GET.get("min_price", None)
        beds = request.GET.get("beds", None)
        bedrooms = request.GET.get("bedrooms", None)
        bathrooms = request.GET.get("bathrooms", None)
        north = request.GET.get("north", None)
        east = request.GET.get("east", None)
        south = request.GET.get("south", None)
        west = request.GET.get("west", None)
        filter_kwargs = {}
        if search is not None:
            filter_kwargs["address__contains"] = search
        if max_price is not None:
            filter_kwargs["pr ice__lte"] = max_price
        if min_price is not None:
            filter_kwargs["price__gte"] = min_price
        if beds is not None:
            filter_kwargs["beds__gte"] = beds
        if bedrooms is not None:
            filter_kwargs["bedrooms__gte"] = bedrooms
        if bathrooms is not None:
            filter_kwargs["bathrooms__gte"] = bathrooms
        paginator = self.paginator
        if (
            north is not None
            and east is not None
            and south is not None
            and west is not None
        ):
            filter_kwargs["lat__gte"] = float(south)
            filter_kwargs["lat__lte"] = float(north)
            filter_kwargs["lng__gte"] = float(west)
            filter_kwargs["lng__lte"] = float(east)
        try:
            rooms = Room.objects.filter(**filter_kwargs)
        except ValueError:
            rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(results, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True)
    def reviews(self, request, uuid):
        room = self.get_object()
        if room:
            try:
                serializer = ReviewSerializer(
                    room.reviews.all().order_by("-created_at"), many=True
                ).data
                return Response(data=serializer, status=status.HTTP_200_OK)
            except Review.DoesNotExist:
                pass

        return Response(status=status.HTTP_400_BAD_REQUEST)
