from django.urls import path
from codingclub_api.apps.competitions.api.v1.views import CompetitionsApiView

urlpatterns = [
    path("v1/competition/", CompetitionsApiView.as_view()),
]
