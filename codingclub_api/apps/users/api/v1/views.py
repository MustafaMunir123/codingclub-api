import uuid
from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework import status
from codingclub_api.apps.users.models import User, OTP
from codingclub_api.apps.email_service import send_email
from codingclub_api.apps.services import (store_image_get_url, delete_image_from_url)
from codingclub_api.apps.users.constants import PROFILE_PIC_ICON
from codingclub_api.apps.clubs.models import Club
from codingclub_api.apps.users.api.v1.serializers import UserSerializer
from codingclub_api.apps.clubs.api.v1.serializers import ClubSerializer
from rest_framework.permissions import (IsAuthenticated, BasePermission)
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

    @staticmethod
    def update_and_delete_pic(picture, old_url):
        if old_url != PROFILE_PIC_ICON:
            path = old_url.split('.com/o/', 1)[1].replace('%2F', '/').replace('%20', ' ')
            path = path.split('?alt')[0]
            delete_image_from_url(path)
        image_url = store_image_get_url(picture[0], "profile_pic/")
        return image_url

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
            image_file = ''
            if request.data['profile_pic'] != '':
                image_file = request.data.pop("profile_pic")
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            if image_file:
                image_url = store_image_get_url(image_file[0], "profile_pic/")
                user = User.objects.get(email=request.data["email"])
                user.profile_pic = image_url
                user.save()
            body = f"Account created successfully for user '{serializer.validated_data['first_name']} {serializer.validated_data['last_name']}'"
            send_email(f"mustafamunir10@gmail.com", f"D-Sync Account for User: {serializer.validated_data['first_name']}", body)
            return success_response(status=status.HTTP_200_OK, data=serializer.validated_data)
        except Exception as ex:
            raise ex

    def patch(self, request, pk):
        try:
            user = User.objects.get(user_id=pk)
            serializer = self.get_serializer()
            if request.data['profile_pic'] != '':
                profile_pic = request.data.pop('profile_pic')
                request.data['profile_pic'] = self.update_and_delete_pic(picture=profile_pic, old_url=user.profile_pic)
            serializer = serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(status=status.HTTP_200_OK, data=serializer.validated_data)
        except Exception as ex:
            raise ex

    @staticmethod
    def delete(request, pk):
        try:
            user = User.objects.get(user_id=pk)
            email = user.email
            user.delete()
            return success_response(status=status.HTTP_200_OK, data=f"User deleted succesfully with email {email}")
        except Exception as ex:
            raise ex


class AdminApiView(APIView):

    @staticmethod
    def get_serializer():
        return UserSerializer

    @staticmethod
    def get_club_serializer():
        return ClubSerializer

    def get_club_requests(self):
        try:
            club_data = Club.objects.filter(is_accepted=False, rejected=False)
            serializer = self.get_club_serializer()
            serializer = serializer(club_data, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def get_rejected_clubs(self):
        try:
            club_data = Club.objects.filter(rejected=True)
            serializer = self.get_club_serializer()
            serializer = serializer(club_data, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def get_admin_users(self):
        users = User.objects.filter(is_admin=True, is_superuser=False)
        serializer = self.get_serializer()
        serializer = serializer(users, many=True)
        return success_response(status=status.HTTP_200_OK, data=serializer.data)

    def get(self, request):
        if "get_club_requests" in request.path:
            return self.get_club_requests()
        elif "get_admin_users" in request.path:
            return self.get_admin_users()
        elif "get_rejected_clubs" in request.path:
            return self.get_rejected_clubs()

    def post(self, request):
        if "user_acceptance" in request.path:
            pass

    def patch(self, request, pk):
        try:
            club = Club.objects.get(id=pk)
            serializer = self.get_club_serializer()
            serializer = serializer(club, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            msg = f"Club '{club.name}' registered successfully"
            if "rejected" in serializer.validated_data:
                msg = f"Club creation request rejected for {club.name}"
            return success_response(status=status.HTTP_200_OK, data=msg)
        except Exception as ex:
            raise ex


class UserUtilsApiView(APIView):

    @staticmethod
    def get_serializer():
        return UserSerializer

    @staticmethod
    def generate_otp(request):
        try:
            otp = f"{str(uuid.uuid4())[:3]}-{str(uuid.uuid4())[:3]}-{str(uuid.uuid4())[:3]}"
            otp = OTP.objects.create(otp=otp)
            body = f"OTP requested by email: {request.data['email']} is '{otp.otp}'"
            send_email(to=f"{request.data['email']}", subject="D-Sync Email validation", body=body)
            return success_response(status=status.HTTP_200_OK, data=f"OTP sent to email: {request.data['email']}")
        except Exception as ex:
            raise ex

    @staticmethod
    def validate_otp(request):
        otp = request.data.pop("otp")
        if OTP.objects.filter(otp=otp).exists():
            return success_response(status=status.HTTP_200_OK, data="email verified")
        return success_response(status=status.HTTP_400_BAD_REQUEST, success=False, data="Invalid OTP")

    def sign_in(self, request):
        check = 0
        try:
            # EmailService.send_email(subject="D-Sync User Account", to="munir4303324@cloud.neduet.edu.pk", to_name="Test User", message="This is a test email")
            user = User.objects.get(email=request.data["email"])
            check = 1
            user = User.objects.get(password=request.data["password"], email=request.data["email"])
            check = 2
            serializer = self.get_serializer()
            serializer = serializer(user)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            if check == 0:
                raise ValueError("Incorrect Email")
            elif check == 1:
                raise ValueError("Incorrect Password")
            raise ex

    def post(self, request):
        if "sign_in" in request.path:
            return self.sign_in(request)
        elif "validate_otp" in request.path:
            return self.validate_otp(request)

    def get(self, request):
        if "generate_otp" in request.path:
            return self.generate_otp(request)
