from django.urls import path, include
from codingclub_api.apps.users.api.v1 import urls as v1_user

urlpatterns = [
    path("user/", include(v1_user)),
]
