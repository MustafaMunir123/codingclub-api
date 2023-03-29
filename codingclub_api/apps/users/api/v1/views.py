from rest_framework.views import Response
from rest_framework.views import APIView
from codingclub_api.apps.users.models import User
from codingclub_api.apps.users.api.v1.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
# Create your views here.


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            if request.user.is_admin:
                return False
        return True


class UserApiView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        data = User.objects.all()
        serializer = UserSerializer(data=data, many=True)
        serializer.is_valid()
        return Response({"data": serializer.data})

