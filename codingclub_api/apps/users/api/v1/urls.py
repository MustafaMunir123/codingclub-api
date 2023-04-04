from django.urls import path
from codingclub_api.apps.users.api.v1.views import UserApiView, AdminApiView


urlpatterns = [
    path("v1/user/", UserApiView.as_view()),
    path("v1/user/<uuid:pk>", UserApiView.as_view()),
    path("v1/club_status/<uuid:pk>", AdminApiView.as_view()),
    path("v1/get_all_clubs/", AdminApiView.as_view()),
    path("v1/get_admin_users/", AdminApiView.as_view()),
]
