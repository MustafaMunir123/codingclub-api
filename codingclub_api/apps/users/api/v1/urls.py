from django.urls import path
from codingclub_api.apps.users.api.v1.views import UserApiView, AdminApiView, UserUtilsApiView


urlpatterns = [
    path("v1/user/", UserApiView.as_view()),
    path("v1/user/<uuid:pk>", UserApiView.as_view()),

    path("v1/sign_in/", UserUtilsApiView.as_view()),
    path("v1/generate_otp/", UserUtilsApiView.as_view()),
    path("v1/validate_otp/", UserUtilsApiView.as_view()),

    path("v1/reject_club_request/", AdminApiView.as_view()),
    path("v1/accept_club_request/", AdminApiView.as_view()),
    path("v1/get_club_requests/", AdminApiView.as_view()),
    path("v1/get_admin_users/", AdminApiView.as_view()),
    path("v1/get_rejected_clubs/", AdminApiView.as_view()),
    path("v1/create_admin_user/", AdminApiView.as_view()),
    path("v1/add_category/", AdminApiView.as_view()),
    path("v1/add_domain/", AdminApiView.as_view()),
    path("v1/add_role/", AdminApiView.as_view()),
]
