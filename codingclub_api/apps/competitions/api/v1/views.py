from rest_framework.views import APIView, status
from codingclub_api.apps.competitions.models import Competition, Competitor
from codingclub_api.apps.utils import success_response
from codingclub_api.apps.competitions.api.v1.serializers import CompetitionSerializer

# Create your views here.


class CompetitionsApiView(APIView):
    @staticmethod
    def update_status(competitions):
        for competition in competitions:
            competition.is_active = False
            competition.save()

    @staticmethod
    def get_serializer():
        return CompetitionSerializer

    @staticmethod
    def create_manytomany_data(unique_param, data):
        obj_ids = []
        for obj_data in data:
            competitor = Competitor.objects.create(**obj_data)
            competitor.save()
            obj_ids.append(competitor.id)
        competition = Competition.objects.get(name=unique_param)
        competition.competitor.add(*obj_ids)

    def get(self, request):
        try:
            competition = Competition.objects.get(is_active=True)
            serializer = self.get_serializer()
            serializer = serializer(competition)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def post(self, request):
        try:
            competitions = Competition.objects.all()
            self.update_status(competitions=competitions)
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.create_manytomany_data(
                unique_param=serializer.validated_data["name"],
                data=request.data.pop("competitor"),
            )
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex
