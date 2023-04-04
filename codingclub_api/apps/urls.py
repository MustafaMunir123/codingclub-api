from django.urls import path, include
from codingclub_api.apps.users.api.v1 import urls as v1_users
from codingclub_api.apps.clubs.api.v1 import urls as v1_clubs

urlpatterns = [
    path("users/", include(v1_users)),
    path("clubs/", include(v1_clubs)),
]
