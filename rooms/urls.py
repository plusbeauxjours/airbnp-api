from django.urls import path
from . import views

app_name = "rooms"

# urlpatterns = [
#     path("list/", views.room_list),
#     path("list/", views.RoomListView.as_view()),
#     path("<int:pk>/", views.RoomDetailView.as_view()),
#     # path("<int:pk>/", views.RoomDetailView.as_view()),
#     path("<uuid:uuid>/", views.RoomDetailView.as_view()),
# ]

from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register("", viewsets.RoomViewset, basename="room")

urlpatterns = router.urls
