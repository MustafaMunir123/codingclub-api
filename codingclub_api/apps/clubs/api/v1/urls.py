from django.urls import path
from codingclub_api.apps.clubs.api.v1.views import (
    ClubApiView,
    ClubMemberApiView,
    ClubDomainsApiView,
    CategoryApiView,
    ClubRoleApiView,
    ClubEventsApiView,
    UserDashboardApiView,
    ClubDashboardApiView,
    EventCalenderApiView,
)

urlpatterns = [
    path("v1/club/", ClubApiView.as_view()),
    path("v1/club/<uuid:pk>", ClubApiView.as_view()),
    path(
        "v1/become_member_of_club/",
        ClubMemberApiView.as_view(),
        name="become_member_of_club",
    ),
    path("v1/domains/", ClubDomainsApiView.as_view()),
    path("v1/categories/", CategoryApiView.as_view()),
    path("v1/roles/", ClubRoleApiView.as_view()),
    path("v1/events/", ClubEventsApiView.as_view()),
    path("v1/events/<uuid:pk>", ClubEventsApiView.as_view()),
    path("v1/clubs_by_user/<uuid:pk>", UserDashboardApiView.as_view()),
    path("v1/club_events_by_user/<uuid:pk>", UserDashboardApiView.as_view()),
    path("v1/user_posts/<uuid:pk>", UserDashboardApiView.as_view()),
    path("v1/club/events/<uuid:pk>", ClubDashboardApiView.as_view()),
    path("v1/club/members/<uuid:pk>", ClubDashboardApiView.as_view()),
    path("v1/club/member_request/<uuid:pk>", ClubDashboardApiView.as_view()),
    path("v1/club/registrations/<uuid:pk>", ClubDashboardApiView.as_view()),
    path("v1/events/calender/", EventCalenderApiView.as_view()),
]
