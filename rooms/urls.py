from rest_framework.routers import DefaultRouter
from . import viewSets

# from . import views
# from django.urls import path

app_name = "rooms"
router = DefaultRouter()
router.register("", viewSets.RoomViewSet)
urlpatterns = router.urls

# urlpatterns = [
#     path("", views.RoomsView.as_view()),
#     path("search/", views.RoomSearchView.as_view()),
#     path("<uuid:uuid>/", views.RoomView.as_view()),
# ]
