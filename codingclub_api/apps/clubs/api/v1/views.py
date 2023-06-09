from datetime import datetime as dt

from rest_framework.views import APIView, status
from codingclub_api.apps.clubs.enums import EventStatus
from rest_framework.permissions import IsAuthenticated
from codingclub_api.apps.users.permissions import IsAdmin
from codingclub_api.apps.clubs.permissions import IsLeadNotGET, IsLead
from codingclub_api.apps.posts.permissions import IsAuthenticatedNotGET

from codingclub_api.apps.clubs.api.v1.serializers import (
    CategorySerializer,
    ClubDomainSerializer,
    ClubEventSerializer,
    ClubMemberSerializer,
    ClubRoleSerializer,
    ClubSerializer,
    EventRegistrationSerializer,
)
from codingclub_api.apps.clubs.api.v1.services import (
    update_event_status,
    structure_event,
    event_name_url,
    EventRegistrationService,
)
from codingclub_api.apps.clubs.models import (
    Category,
    Club,
    ClubDomain,
    ClubEvent,
    ClubMember,
    ClubRole,
    EventRegistration,
)
from codingclub_api.apps.posts.api.v1.serializers import PostSerializer
from codingclub_api.apps.posts.models import Post
from codingclub_api.apps.email_service import send_email
from codingclub_api.apps.services import (
    convert_to_id,
    store_image_get_url,
    format_image_url,
    delete_image_from_url,
)
from codingclub_api.apps.typings import SuccessResponse
from codingclub_api.apps.users.api.v1.serializers import UserSerializer
from codingclub_api.apps.users.models import User
from codingclub_api.apps.utils import success_response


class ClubApiView(APIView):
    permission_classes = [IsAuthenticatedNotGET]

    @staticmethod
    def set_id(model, unique_param, validate_data) -> None:
        obj = model.objects.get(name=unique_param)
        validate_data["id"] = obj.id

    @staticmethod
    def get_serializer():
        return ClubSerializer

    def get(self, request, pk=None) -> SuccessResponse:
        try:
            serializer = self.get_serializer()
            if pk is not None:
                queryset = Club.objects.get(id=pk, is_accepted=True)
                serializer = serializer(queryset)
                return success_response(status=status.HTTP_200_OK, data=serializer.data)
            queryset = Club.objects.filter(is_accepted=True)
            serializer = serializer(queryset, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def post(self, request) -> SuccessResponse:
        try:
            logo = request.data.pop("logo")
            banner = request.data.pop("banner")
            category = {"tags": request.data.pop("category")[0]}
            role = {"role": request.data.pop("roles")[0]}
            domain = {"domain": request.data.pop("domains")[0]}
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
            club_data["lead_user"] = UserSerializer(user_data).data

            self.set_id(
                Club, serializer.validated_data["name"], serializer.validated_data
            )

            club = Club.objects.get(id=serializer.validated_data["id"])
            category_list = convert_to_id(
                dictionary_list=category, ManyToManyModel=Category
            )
            club.category.add(*category_list)
            domain_list = convert_to_id(
                dictionary_list=domain, ManyToManyModel=ClubDomain
            )
            club.domain.add(*domain_list)
            role_list = convert_to_id(dictionary_list=role, ManyToManyModel=ClubRole)
            club.role.add(*role_list)
            club.save()
            return success_response(status=status.HTTP_200_OK, data=club_data)
        except Exception as ex:
            raise ex

    @staticmethod
    def delete(request, pk):
        try:
            club = Club.objects.get(id=pk)
            club.delete()
            return success_response(
                status=status.HTTP_200_OK, data="Deleted successfully"
            )
        except Exception as ex:
            return ex

    def patch(self, request, pk):
        try:
            club = Club.objects.get(id=pk)
            if "logo" in request.data:
                logo = request.data.pop("logo")
                path = format_image_url(url=club.logo)
                delete_image_from_url(url_path=path)
                request.data["logo"] = store_image_get_url(
                    image_file=logo[0], path="clubs/logo/"
                )
            if "banner" in request.data:
                banner = request.data.pop("banner")
                path = format_image_url(url=club.banner)
                delete_image_from_url(url_path=path)
                request.data["banner"] = store_image_get_url(
                    image_file=banner[0], path="clubs/banner/"
                )
            serializer = self.get_serializer()
            serializer = serializer(club, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            return ex


class ClubMemberApiView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_serializer():
        return ClubMemberSerializer

    def post(self, request) -> SuccessResponse:
        response = success_response(status=status.HTTP_200_OK, data=None)
        if "become_member_of_club" in request.path:
            response = self.become_member_of_club(request)
        return response

    def become_member_of_club(self, request) -> SuccessResponse:
        try:
            user_id = request.data["user_id"]
            club_id = request.data["club_id"]
            user, club = User.objects.get(user_id=user_id), Club.objects.get(id=club_id)
            if user.is_lead:
                lead_club = Club.objects.get(lead_user=user)
                return success_response(
                    status=status.HTTP_400_BAD_REQUEST,
                    success=False,
                    data=f"User with email: {user.email} is leading  {lead_club.name},"
                    f" so user cannot join any other clubs.",
                )

            member_of_clubs = ClubMember.objects.filter(user=user)
            for club_member in member_of_clubs:
                if club_member.club == club:
                    # TODO: implement failure_response
                    return success_response(
                        status=status.HTTP_400_BAD_REQUEST,
                        success=False,
                        data=f"Already a part of {club}",
                    )

            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex
        pass


class ClubDomainsApiView(APIView):
    permission_classes = [IsAdmin]

    @staticmethod
    def get_serializer():
        return ClubDomainSerializer

    def get(self, request) -> SuccessResponse:
        try:
            domains = ClubDomain.objects.all()
            serializer = self.get_serializer()
            serializer = serializer(domains, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def post(self, request):
        try:
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex


class CategoryApiView(APIView):
    permission_classes = [IsAdmin]

    @staticmethod
    def get_serializer():
        return CategorySerializer

    def get(self, request) -> SuccessResponse:
        try:
            categories = Category.objects.all()
            serializer = self.get_serializer()
            serializer = serializer(categories, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def post(self, request):
        try:
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex


class ClubRoleApiView(APIView):
    permission_classes = [IsAdmin]

    @staticmethod
    def get_serializer():
        return ClubRoleSerializer

    def get(self, request) -> SuccessResponse:
        try:
            roles = ClubRole.objects.all()
            serializer = self.get_serializer()
            serializer = serializer(roles, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def post(self, request):
        try:
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex


class ClubEventsApiView(APIView):
    permission_classes = [IsAuthenticated, IsLeadNotGET]

    @staticmethod
    def get_serializer():
        return ClubEventSerializer

    def get(self, request, pk=None) -> SuccessResponse:
        date_today = dt.today().date()
        serializer = self.get_serializer()
        if pk is not None:
            event = ClubEvent.objects.filter(of_club=pk)
            updated_event = update_event_status(events=event, date_today=date_today)
            serializer = serializer(updated_event, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        events = ClubEvent.objects.all()
        updated_events = update_event_status(events=events, date_today=date_today)
        serializer = serializer(updated_events, many=True)
        return success_response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        try:
            if "banner" in request.data:
                banner = request.data.pop("banner")
                request.data["banner"] = store_image_get_url(
                    image_file=banner[0], path="clubs/events/banner/"
                )
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex

    def patch(self, request, pk):
        try:
            event = ClubEvent.objects.get(id=pk)
            if "banner" in request.data:
                banner = request.data.pop("banner")
                path = format_image_url(url=event.banner)
                delete_image_from_url(url_path=path)
                request.data["banner"] = store_image_get_url(
                    image_file=banner[0], path="clubs/events/banner/"
                )
            serializer = self.get_serializer()
            serializer = serializer(event, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex


class UserDashboardApiView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def clubs_by_user(request, pk) -> SuccessResponse or Exception:
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
    def club_events_by_user(request, pk) -> SuccessResponse:
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
    def user_posts(request, pk) -> SuccessResponse:
        try:
            user = User.objects.get(user_id=pk)
            posts = Post.objects.filter(author=user)
            serializer = PostSerializer(posts, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def get(self, request, pk=None) -> SuccessResponse:
        if "clubs_by_user" in request.path:
            return self.clubs_by_user(request, pk)
        elif "club_events_by_user" in request.path:
            return self.club_events_by_user(request, pk)
        elif "user_posts" in request.path:
            return self.user_posts(request, pk)


class ClubDashboardApiView(APIView):
    permission_classes = [IsAuthenticated, IsLead]

    @staticmethod
    def events(request, pk) -> SuccessResponse:
        try:
            club = Club.objects.get(id=pk)
            events = ClubEvent.objects.filter(of_club=club)
            serializer = ClubEventsApiView.get_serializer()
            serializer = serializer(events, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    @staticmethod
    def members(request, pk) -> SuccessResponse:
        try:
            club = Club.objects.get(is_accepted=True, id=pk)
            members = ClubMember.objects.filter(club=club, is_accepted=True)
            serializer = ClubMemberApiView.get_serializer()
            serializer = serializer(members, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    @staticmethod
    def member_request(request, pk) -> SuccessResponse:
        try:
            club = Club.objects.get(is_accepted=True, id=pk)
            print(club)
            members = ClubMember.objects.filter(club=club, is_accepted=False)
            serializer = ClubMemberApiView.get_serializer()
            serializer = serializer(members, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    @staticmethod
    def registrations(request, pk) -> SuccessResponse:
        try:
            club = Club.objects.get(is_accepted=True, id=pk)
            events = ClubEvent.objects.filter(of_club=club)
            registrations = []
            for event in events:
                registrations_of_event = EventRegistration.objects.filter(
                    of_event=event
                )
                registrations.extend(registrations_of_event)
            serializer = EventRegistrationApiView.get_serializer()
            serializer = serializer(registrations, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    @staticmethod
    def domains_by_clubs(request, pk):
        try:
            club = Club.objects.get(id=pk)
            club_domains = club.domain.all()
            serializer = ClubDomainSerializer(club_domains, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    @staticmethod
    def roles_by_clubs(request, pk):
        try:
            club = Club.objects.get(id=pk)
            club_roles = club.role.all()
            serializer = ClubRoleSerializer(club_roles, many=True)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def get(self, request, pk=None):
        if "events" in request.path:
            return self.events(request, pk)
        elif "members" in request.path:
            return self.members(request, pk)
        elif "member_request" in request.path:
            return self.member_request(request, pk)
        elif "registrations" in request.path:
            return self.registrations(request, pk)
        elif "domains_by_clubs" in request.path:
            return self.domains_by_clubs(request, pk)
        elif "roles_by_clubs" in request.path:
            return self.roles_by_clubs(request, pk)

    @staticmethod
    def contact_club(request):
        try:
            subject = "D-Sync: Someone's trying to contact through your club"
            body = f"Some one with email {request.data['email']} has following query:\n {request.data['query']}"
            send_email(to=request.data.pop("lead_email"), subject=subject, body=body)
            return success_response(
                status=status.HTTP_200_OK, data="Email send to lead user"
            )
        except Exception as ex:
            return ex

    def post(self, request):
        if "contact_club" in request.path:
            return self.contact_club(request)


class EventCalenderApiView(APIView):
    @staticmethod
    def calender(request):
        try:
            events = ClubEvent.objects.filter(
                registration_status=EventStatus.UPCOMMING.value
            )
            serializer = ClubEventSerializer(events, many=True)
            data = structure_event(events=serializer.data)
            return success_response(status=status.HTTP_200_OK, data=data)
        except Exception as ex:
            return ex

    def get(self, request):
        if "events/calender" in request.path:
            return self.calender(request)


class ImageGalleryApiView(APIView):
    @staticmethod
    def gallery(request):
        try:
            events = ClubEvent.objects.all()
            serializer = ClubEventSerializer(events, many=True)
            data = event_name_url(events=serializer.data)
            print(data)
            return success_response(status=status.HTTP_200_OK, data=data)
        except Exception as ex:
            raise ex

    def get(self, request):
        if "events/gallery" in request.path:
            return self.gallery(request)


class EventRegistrationApiView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_serializer():
        return EventRegistrationSerializer

    def post(self, request):
        try:
            event = ClubEvent.objects.get(id=request.data["of_event_id"])
            if EventRegistrationService.check_seats_limit(
                registrations=request.data["registration_for_user"],
                registered_seats=event.registrations_made,
                total_seats=event.no_of_registrations,
            ):
                raise ValueError(f"Not enough seats left for event {event.name}")
            data, errors = EventRegistrationService.structure_registrations(
                request.data
            )
            if errors:
                raise ValueError(f"Registration already exists for user: {errors}")
            event.registrations_made += len(data)
            event.save()
            serializer = self.get_serializer()
            serializer = serializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(serializer.validated_data)
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex
