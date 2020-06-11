from . import viewSets
from rest_framework.routers import DefaultRouter

# from . import views
# from django.urls import path

app_name = "users"
router = DefaultRouter()
router.register("", viewSets.UserViewSet)
urlpatterns = router.urls

# urlpatterns = [
#     path("", views.UsersView.as_view()),
#     path("token/", views.Login.as_view()),
#     path("<uuid:uuid>", views.UserView.as_view()),
# ]
