from django.urls import path, include
from codingclub_api.apps.users.api.v1 import urls as v1_users
from codingclub_api.apps.clubs.api.v1 import urls as v1_clubs
from codingclub_api.apps.posts.api.v1 import urls as v1_posts

urlpatterns = [
    path("users/", include(v1_users)),
    path("clubs/", include(v1_clubs)),
    path("posts/", include(v1_posts)),
]
