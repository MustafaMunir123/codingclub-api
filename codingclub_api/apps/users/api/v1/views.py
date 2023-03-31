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

    def get(self, request, pk=None):
        try:
            serializer = self.get_serializer()
            if pk is not None:
                queryset = User.objects.get(user_id=pk)
                serializer = serializer(queryset)
                return success_response(status=status.HTTP_200_OK, data=serializer.data)
            queryset = User.objects.all()
            serializer = serializer(queryset, many=True)
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

    def patch(self, request, pk):
        try:
            user = User.objects.get(user_id=pk)
            serializer = self.get_serializer()
            serializer = serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(status=status.HTTP_200_OK, data=serializer.validated_data)
        except Exception as ex:
            raise ex

    def edit_profile_pic(self, request):
        pass

    def dispatch(self, request, *args, **kwargs):
        # override the dispatch method to handle the custom view
        if request.method.lower() == 'edit_profile_pic':
            return self.edit_profile_pic(request)
        return super().dispatch(request, *args, **kwargs)