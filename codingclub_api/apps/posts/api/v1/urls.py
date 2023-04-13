from django.urls import path
from codingclub_api.apps.posts.api.v1.views import PostApiView

urlpatterns = [
    path("v1/post/", PostApiView.as_view()),
    path("v1/post/<uuid:pk>", PostApiView.as_view()),
]
