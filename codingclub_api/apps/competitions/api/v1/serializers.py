from rest_framework import serializers
from codingclub_api.apps.competitions.models import Competition, Competitor


class CompetitorSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    ranking = serializers.IntegerField()
    name = serializers.CharField(max_length=100, allow_blank=False, allow_null=False)
    email = serializers.EmailField(max_length=100, allow_null=False, allow_blank=False)

    def create(self, validated_data):
        competitor = Competitor.objects.create(**validated_data)
        return competitor


class CompetitionSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=70, allow_blank=False, allow_null=False)
    organized_by = serializers.CharField(
        max_length=70, allow_null=False, allow_blank=False
    )
    is_active = serializers.BooleanField(allow_null=False)
    competitor = CompetitorSerializer(read_only=True, many=True)
    # competitor_id = serializers.UUIDField(allow_null=True)

    def create(self, validated_data):
        print(validated_data)
        # for competitor in validated_data.pop("competitor"):
        #     Competitor.objects.create(**competitor)
        competition = Competition.objects.create(**validated_data)
        return competition
