from django.urls import path
from rest_framework.routers import SimpleRouter
from codingclub_api.apps.users.api.v1.views import UserApiView

router = SimpleRouter()

urlpatterns = [
    path("v1/", UserApiView.as_view()),
    path("v1/<uuid:pk>", UserApiView.as_view()),
]
