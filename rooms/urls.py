from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("", views.RoomsView.as_view()),
    path("search/", views.RoomSearchView.as_view()),
    path("<uuid:uuid>/", views.RoomView.as_view()),
]
