import ast
from typing import Dict
from datetime import datetime as dt
from django.forms.models import model_to_dict
from rest_framework.views import (
    APIView,
    status,
)
from codingclub_api.apps.services import convert_to_id
from codingclub_api.apps.utils import success_response
from codingclub_api.apps.clubs.enums import EventStatus
from codingclub_api.apps.posts.models import Post
from codingclub_api.apps.clubs.api.v1.services import update_event_status
from codingclub_api.apps.posts.api.v1.serializers import PostSerializer
from codingclub_api.apps.clubs.models import (
    Club,
    Category,
    ClubDomain,
    ClubRole,
    ClubMember,
    ClubEvent
)
from codingclub_api.apps.clubs.api.v1.serializers import (
    ClubSerializer,
    ClubMemberSerializer,
    ClubDomainSerializer,
    CategorySerializer,
    ClubRoleSerializer,
    ClubEventSerializer
)
from codingclub_api.apps.services import store_image_get_url
from codingclub_api.apps.users.models import User
from codingclub_api.apps.users.api.v1.serializers import UserSerializer


class ClubApiView(APIView):
    @staticmethod
    def set_id(model, unique_param, validate_data):
        obj = model.objects.get(name=unique_param)
        validate_data['id'] = obj.id
        return

    @staticmethod
    def add_roles(roles_list, pk):
        roles = []
        roles_list = ast.literal_eval(roles_list)
        for role in roles_list:
            role = ClubRole.objects.get(role=role)
            roles.append(role.id)
        club = Club.objects.get(id=pk)
        club.category.add(*roles)
        club.save()

    @staticmethod
    def add_domains(domains_list, pk):
        domains = []
        domains_list = ast.literal_eval(domains_list)
        for domain in domains_list:
            domain = Category.objects.get(tags=domain)
            domains.append(domain.id)
        club = Club.objects.get(id=pk)
        club.category.add(*domains)
        club.save()


    @staticmethod
    def get_serializer():
        return ClubSerializer

    def get(self, request, pk=None):
        try:
            serializer = self.get_serializer()
            if pk is not None:
                queryset = Club.objects.get(id=pk)
                serializer = serializer(queryset)
                return success_response(status=status.HTTP_200_OK, data=serializer.data)
            queryset = Club.objects.all()
            serializer = serializer(queryset, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def post(self, request):
        try:
            logo = request.data.pop("logo")
            banner = request.data.pop("banner")
            category = {'tags': request.data.pop("category")[0]}
            role = {'role': request.data.pop("roles")[0]}
            domain = {'domain': request.data.pop("domains")[0]}
            request.data["logo"] = store_image_get_url(logo[0], "clubs/logo/")
            request.data["banner"] = store_image_get_url(banner[0], "clubs/banner/")

            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_data = User.objects.get(user_id=request.data["lead_user"])
            user_data.is_lead = True
            user_data.save()
            serializer.validated_data["lead_user"] = user_data
            serializer.save()
            club_data = serializer.data
            club_data['lead_user'] = UserSerializer(user_data).data

            self.set_id(Club, serializer.validated_data['name'], serializer.validated_data)

            club = Club.objects.get(id=serializer.validated_data["id"])
            category_list = convert_to_id(dictionary_list=category, ManyToManyModel=Category)
            club.category.add(*category_list)
            domain_list = convert_to_id(dictionary_list=domain, ManyToManyModel=ClubDomain)
            club.domain.add(*domain_list)
            role_list = convert_to_id(dictionary_list=role, ManyToManyModel=ClubRole)
            club.role.add(*role_list)
            club.save()
            return success_response(status=status.HTTP_200_OK, data=club_data)
        except Exception as ex:
            raise ex


class ClubMemberApiView(APIView):
    @staticmethod
    def get_serializer():
        return ClubMemberSerializer

    def post(self, request):
        response = success_response(status=status.HTTP_200_OK, data=None)
        if "become_member_of_club" in request.path:
            response = self.become_member_of_club(request)
        return response

    def become_member_of_club(self, request):
        try:
            user_id = request.data["user_id"]
            club_id = request.data["club_id"]
            user, club = User.objects.get(user_id=user_id), Club.objects.get(id=club_id)
            if user.is_lead:
                lead_club = Club.objects.get(lead_user=user)
                return success_response(status=status.HTTP_400_BAD_REQUEST, success=False, data=f"User with email: {user.email} is leading  {lead_club.name}, so user cannot join any other clubs.")

            member_of_clubs = ClubMember.objects.filter(user=user)
            for club_member in member_of_clubs:
                if club_member.club == club:
                    # TODO: implement failure_response
                    return success_response(status=status.HTTP_400_BAD_REQUEST, success=False, data=f"Already a part of {club}")

            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(status=status.HTTP_200_OK, data=serializer.validated_data)
        except Exception as ex:
            raise ex
        pass


class ClubDomainsApiView(APIView):
    @staticmethod
    def get_serializer():
        return ClubDomainSerializer

    def get(self, request):
        try:
            domains = ClubDomain.objects.all()
            serializer = self.get_serializer()
            serializer = serializer(domains, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex


class CategoryApiView(APIView):
    @staticmethod
    def get_serializer():
        return CategorySerializer

    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = self.get_serializer()
            serializer = serializer(categories, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex


class ClubRoleApiView(APIView):
    @staticmethod
    def get_serializer():
        return ClubRoleSerializer

    def get(self, request):
        try:
            roles = ClubRole.objects.all()
            serializer = self.get_serializer()
            serializer = serializer(roles, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex


class ClubEventsApiView(APIView):
    @staticmethod
    def get_serializer():
        return ClubEventSerializer

    def get(self, request, pk=None):
        date_today = dt.today().date()
        serializer = self.get_serializer()
        if pk is not None:
            event = ClubEvent.objects.filter(id=pk)
            updated_event = update_event_status(events=event, date_today=date_today)
            serializer = serializer(updated_event, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        events = ClubEvent.objects.all()
        updated_events = update_event_status(events=events, date_today=date_today)
        serializer = serializer(updated_events, many=True)
        return success_response(status=status.HTTP_200_OK, data=serializer.data)


class UserDashboardApiView(APIView):

    @staticmethod
    def clubs_by_user(request, pk):
        try:
            user = User.objects.get(user_id=pk)
            club_members = ClubMember.objects.filter(user=user)
            club_ids = [club.club.id for club in club_members]
            clubs = Club.objects.filter(pk__in=club_ids)
            serializer = ClubApiView.get_serializer()
            serializer = serializer(clubs, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            return ex

    @staticmethod
    def club_events_by_user(request,pk):
        try:
            user = User.objects.get(user_id=pk)
            club_members = ClubMember.objects.filter(user=user)
            club_ids = [club.club.id for club in club_members]
            clubs = Club.objects.filter(pk__in=club_ids)
            event_ids = []
            for club in clubs:
                events = ClubEvent.objects.filter(of_club=club)
                for event in events:
                    event_ids.append(event.id)
            events = ClubEvent.objects.filter(pk__in=event_ids)
            serializer = ClubEventsApiView.get_serializer()
            serializer = serializer(events, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    @staticmethod
    def user_posts(request, pk):
        try:
            user = User.objects.get(user_id=pk)
            posts = Post.objects.filter(author=user)
            serializer = PostSerializer(posts, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def get(self, request, pk=None):
        if "clubs_by_user" in request.path:
            return self.clubs_by_user(request, pk)
        elif "club_events_by_user" in request.path:
            return self.club_events_by_user(request, pk)
        elif "user_posts" in request.path:
            return self.user_posts(request, pk)
