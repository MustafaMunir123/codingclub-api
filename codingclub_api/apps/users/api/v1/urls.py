from django.urls import path
from codingclub_api.apps.users.api.v1.views import UserApiView, AdminApiView, UserUtilsApiView


urlpatterns = [
    path("v1/user/", UserApiView.as_view()),
    path("v1/user/<uuid:pk>", UserApiView.as_view()),

    path("v1/sign_in/", UserUtilsApiView.as_view()),
    path("v1/generate_otp/", UserUtilsApiView.as_view()),
    path("v1/validate_otp/", UserUtilsApiView.as_view()),
    path("v1/reject_club_request/", AdminApiView.as_view()),

    path("v1/club_status/<uuid:pk>", AdminApiView.as_view()),
    path("v1/get_club_requests/", AdminApiView.as_view()),
    path("v1/get_admin_users/", AdminApiView.as_view()),
    path("v1/get_rejected_clubs/", AdminApiView.as_view()),
]
