from django.urls import path
from codingclub_api.apps.clubs.api.v1.views import ClubApiView, ClubMemberApiView


urlpatterns = [
    path("v1/club/", ClubApiView.as_view()),
    path("v1/club/<uuid:pk>", ClubApiView.as_view()),
    path("v1/become_member_of_club/", ClubMemberApiView.as_view(), name="become_member_of_club"),
]
