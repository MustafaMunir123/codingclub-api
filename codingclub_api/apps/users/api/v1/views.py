import base64
from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework import status
from codingclub_api.apps.users.models import User
from codingclub_api.apps.users.services import store_image_get_url
from codingclub_api.apps.users.api.v1.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from codingclub_api.apps.utils import success_response
# Create your views here.


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            if request.user.is_admin:
                return False
        return True


class UserApiView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @staticmethod
    def get_serializer():
        return UserSerializer

    def get(self, request):
        try:
            data = User.objects.all()
            serializer = self.get_serializer()
            store_image_get_url("test", "one")
            serializer = serializer(data=data, many=True)
            serializer.is_valid()
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def post(self, request):
        try:
            image_file = request.FILES["profile_pic"]
            request.data.pop("profile_pic")
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            image_url = store_image_get_url(image_file, "profile_pic/")
            user = User.objects.get(email=request.data["email"])
            user.profile_pic = image_url
            user.save()
            return success_response(status=status.HTTP_200_OK, data=serializer.validated_data)
        except Exception as ex:
            raise ex
