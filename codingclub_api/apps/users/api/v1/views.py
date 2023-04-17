import uuid

from rest_framework import status

# from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from codingclub_api.apps.clubs.api.v1.serializers import (
    CategorySerializer,
    ClubDomainSerializer,
    ClubRoleSerializer,
    ClubSerializer,
)
from codingclub_api.apps.clubs.models import Club
from codingclub_api.apps.email_service import send_email
from codingclub_api.apps.services import (
    delete_image_from_url,
    format_image_url,
    store_image_get_url,
)
from codingclub_api.apps.typings import SuccessResponse
from codingclub_api.apps.users.api.v1.serializers import UserSerializer
from codingclub_api.apps.users.constants import PROFILE_PIC_ICON
from codingclub_api.apps.users.models import OTP, User

# from codingclub_api.apps.users.permissions import IsSuperAdmin
from codingclub_api.apps.utils import CacheUtils, success_response


# Create your views here.


class UserApiView(APIView):
    # permission_classes = [IsAuthenticated, IsSuperAdmin]

    @staticmethod
    def get_serializer():
        return UserSerializer

    @staticmethod
    def update_and_delete_pic(picture, old_url) -> str:
        if old_url != PROFILE_PIC_ICON:
            path = format_image_url(url=old_url)
            delete_image_from_url(path)
        image_url = store_image_get_url(picture[0], "profile_pic/")
        return image_url

    def get(self, request, pk=None) -> SuccessResponse:
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

    def post(self, request) -> SuccessResponse:
        try:
            serializer = self.get_serializer()
            serializer = serializer(data=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            body = (
                f"Account created successfully for user '{serializer.validated_data['first_name']} "
                f"{serializer.validated_data['last_name']}'"
            )
            send_email(
                to="mustafamunir10@gmail.com",
                subject=f"D-Sync Account for User: {serializer.validated_data['first_name']}",
                body=body,
            )
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex

    def patch(self, request, pk) -> SuccessResponse:
        try:
            user = User.objects.get(user_id=pk)
            serializer = self.get_serializer()
            if "profile_pic" in request.data:
                if request.data["profile_pic"] != "":
                    profile_pic = request.data.pop("profile_pic")
                    request.data["profile_pic"] = self.update_and_delete_pic(
                        picture=profile_pic, old_url=user.profile_pic
                    )
            serializer = serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex

    @staticmethod
    def delete(request, pk) -> SuccessResponse:
        try:
            user = User.objects.get(user_id=pk)
            url_path = format_image_url(user.profile_pic)
            delete_image_from_url(url_path=url_path)
            email = user.email
            user.delete()
            return success_response(
                status=status.HTTP_200_OK,
                data=f"User deleted successfully with email {email}",
            )
        except Exception as ex:
            raise ex


class AdminApiView(APIView):
    @staticmethod
    def get_serializer():
        return UserSerializer

    @staticmethod
    def get_club_serializer():
        return ClubSerializer

    @staticmethod
    def get_category_serializer():
        return CategorySerializer

    @staticmethod
    def get_domain_serializer():
        return ClubDomainSerializer

    @staticmethod
    def get_role_serializer():
        return ClubRoleSerializer

    def get_club_requests(self) -> SuccessResponse:
        try:
            club_data = Club.objects.filter(is_accepted=False, rejected=False)
            serializer = self.get_club_serializer()
            serializer = serializer(club_data, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def get_rejected_clubs(self) -> SuccessResponse:
        try:
            club_data = Club.objects.filter(rejected=True)
            serializer = self.get_club_serializer()
            serializer = serializer(club_data, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def get_admin_users(self) -> SuccessResponse:
        users = User.objects.filter(is_admin=True, is_superuser=False)
        serializer = self.get_serializer()
        serializer = serializer(users, many=True)
        return success_response(status=status.HTTP_200_OK, data=serializer.data)

    @staticmethod
    def accept_club_request(request) -> SuccessResponse:
        try:
            club = Club.objects.get(id=request.data["id"])
            club.is_accepted = True
            club.save()
            body = f"Congratulations your club request for club {request.data['name']} has been approved by D-Sync team"
            send_email(
                to=f"{request.data['lead_user']['email']}",
                subject="D-Sync: Club Request Approved",
                body=body,
            )
            return success_response(
                status=status.HTTP_200_OK, data="Club successfully approved"
            )
        except Exception as ex:
            raise ex

    def get(self, request) -> SuccessResponse:
        if "get_club_requests" in request.path:
            return self.get_club_requests()
        elif "get_admin_users" in request.path:
            return self.get_admin_users()
        elif "get_rejected_clubs" in request.path:
            return self.get_rejected_clubs()
        elif "accept_club_request" in request.path:
            return self.accept_club_request(request)

    @staticmethod
    def reject_club_request(request) -> SuccessResponse:
        try:
            club = Club.objects.get(id=request.data["id"])
            club.rejected = True
            club.save()
            subject = f"Club Creation Request for {club.name}"
            body = (
                f"Club Creation request by user {request.data['lead_user']['first_name']} "
                f"{request.data['lead_user']['last_name']} for {club.name} rejected because of "
                f"following reason: \n {request.data['reason']}"
            )
            send_email(
                to=f"{request.data['lead_user']['email']}", subject=subject, body=body
            )
            return success_response(
                status=status.HTTP_200_OK, data="Email response sent successfully"
            )
        except Exception as ex:
            raise ex

    @staticmethod
    def create_admin_user(request) -> SuccessResponse:
        admin_check = {"is_admin": True}
        request.data.update(admin_check)
        return UserApiView.post(self=UserApiView(), request=request)

    def add_category(self, request) -> SuccessResponse:
        try:
            serializer = self.get_category_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex

    def add_domain(self, request) -> SuccessResponse:
        try:
            serializer = self.get_domain_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex

    def add_role(self, request):
        try:
            serializer = self.get_role_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex

    def post(self, request, pk=None) -> SuccessResponse:
        if "reject_club_request" in request.path:
            return self.reject_club_request(request)
        elif "create_admin_user" in request.path:
            return self.create_admin_user(request)
        elif "add_category" in request.path:
            return self.add_category(request)
        elif "add_role" in request.path:
            return self.add_role(request)
        elif "add_domain" in request.path:
            return self.add_domain(request)


class UserUtilsApiView(APIView):
    # TODO: scale OTP generation and validation as methods using DRY approach

    @staticmethod
    def generate_otp(request) -> SuccessResponse:
        try:
            CacheUtils.set_cache(cache_key=request.data["email"], data=request.data)
            otp = f"{str(uuid.uuid4())[:3]}-{str(uuid.uuid4())[:3]}-{str(uuid.uuid4())[:3]}"
            otp = OTP.objects.create(otp=otp)
            CacheUtils.set_cache(cache_key=otp, data=otp)
            body = f"OTP requested by email: {request.data['email']} is '{otp.otp}'"
            send_email(
                to="mustafamunir10@gmail.com",
                subject="D-Sync OTP validation",
                body=body,
            )
            return success_response(
                status=status.HTTP_200_OK,
                data=f"OTP sent to email: {request.data['email']}",
            )
        except Exception as ex:
            raise ex

    @staticmethod
    def validate_otp(request) -> SuccessResponse:
        otp = request.data.pop("otp")
        if OTP.objects.filter(otp=otp).exists():
            cached_otp = CacheUtils.get_cache(cache_key=otp)
            if cached_otp:
                cached_data = CacheUtils.get_cache(cache_key=request.data["email"])
                return UserApiView.post(self=UserApiView(), request=cached_data)
            return success_response(
                status=status.HTTP_400_BAD_REQUEST, success=False, data="OTP Expired"
            )
        return success_response(
            status=status.HTTP_400_BAD_REQUEST, success=False, data="Invalid OTP"
        )

    def post(self, request) -> SuccessResponse:
        if "validate_otp" in request.path:
            return self.validate_otp(request)

    def get(self, request) -> SuccessResponse:
        if "generate_otp" in request.path:
            return self.generate_otp(request)


class UserSignInApiView(APIView):
    @staticmethod
    def get_serializer():
        return UserSerializer

    def sign_in(self, request) -> SuccessResponse:
        check = 0
        try:
            user = User.objects.get(email=request.data["email"])
            check = 1
            user = User.objects.get(
                password=request.data["password"], email=request.data["email"]
            )
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

    @staticmethod
    def validate_otp(request) -> SuccessResponse:
        otp = request.data.pop("otp")
        if OTP.objects.filter(otp=otp).exists():
            cached_otp = CacheUtils.get_cache(cache_key=otp)
            if cached_otp:
                cached_data = CacheUtils.get_cache(cache_key=request.data.pop("email"))
                if cached_data:
                    user = User.objects.get(email=cached_data["email"])
                    return UserApiView.patch(
                        self=UserApiView(), request=request, pk=user.user_id
                    )
                return UserApiView.post(self=UserApiView(), request=cached_data)
            return success_response(
                status=status.HTTP_400_BAD_REQUEST, success=False, data="OTP Expired"
            )
        return success_response(
            status=status.HTTP_400_BAD_REQUEST, success=False, data="Invalid OTP"
        )

    def post(self, request):
        if "sign_in" in request.path:
            return self.sign_in(request)
        elif "forget_password" in request.path:
            return self.validate_otp(request)
