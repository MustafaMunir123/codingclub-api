from django.urls import path
from codingclub_api.apps.users.api.v1.views import UserApiView


urlpatterns = [
    path("v1/user/", UserApiView.as_view()),
    path("v1/user/<uuid:pk>", UserApiView.as_view()),
]
