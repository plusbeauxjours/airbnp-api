from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("", views.room_view),
    # path("list/", views.room_list),
    # path("list/", views.ReadRoomListView.as_view()),
    # path("<int:pk>/", views.ReadRoomDetailView.as_view()),
    # path("<int:pk>/", views.RoomDetailView.as_view()),
    # path("<uuid:uuid>/", views.ReadRoomDetailView.as_view()),
]

# from rest_framework.routers import DefaultRouter
# from . import viewsets

# router = DefaultRouter()
# router.register("", viewsets.RoomViewset, basename="room")

# urlpatterns = router.urls
