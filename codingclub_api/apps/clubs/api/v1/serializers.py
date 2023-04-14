from rest_framework import serializers
from codingclub_api.apps.clubs.models import (
    Club,
    ClubMember,
    Category,
    ClubDomain,
    ClubRole,
)
from codingclub_api.apps.users.api.v1.serializers import UserSerializer


class CategorySerializer(serializers.Serializer):
    tags = serializers.CharField(max_length=40)

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category


class ClubRoleSerializer(serializers.Serializer):
    role = serializers.CharField(max_length=40)

    def create(self, validated_data):
        role = ClubRole.objects.create(**validated_data)
        return role


class ClubDomainSerializer(serializers.Serializer):
    domain = serializers.CharField(max_length=40)

    def create(self, validated_data):
        domain = ClubDomain.objects.create(**validated_data)
        return domain


class ClubSerializer(serializers.Serializer):
    logo = serializers.CharField(max_length=400)
    banner = serializers.CharField(max_length=400)
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(max_length=40)
    description = serializers.CharField(max_length=200)
    lead_user = UserSerializer(read_only=True, many=False)
    category = CategorySerializer(many=True, read_only=True)
    domain = ClubDomainSerializer(many=True, read_only=True)
    role = ClubRoleSerializer(many=True, read_only=True)
    is_accepted = serializers.BooleanField(default=False, allow_null=True)
    rejected = serializers.BooleanField(default=False, allow_null=True)

    def create(self, validated_data):
        club = Club.objects.create(**validated_data)
        return club

    def update(self, instance, validated_data):
        # print(f"{instance}-------------------------")
        club = Club.objects.filter(id=instance.id).update(**validated_data)
        return club


class ClubMemberSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    club = ClubSerializer(read_only=True)
    user_id = serializers.CharField(max_length=40, allow_null=True)
    """
    This a really great way of getting foreign many to one data. We do not have user_id & club_id but on passing these
    with there will actually somehow query it automatically to get object.
    this is happening inside create method of serializer because i have set the related_name fields to:
    club for club
    user of user
    so it is actually querying back to club & user model and getting its instance

    e.g. ClubMember.objects.user_id

    NOTE: use of serializers.CharField() is must instead of serializer class
    """
    club_id = serializers.CharField(max_length=40, allow_null=True)
    is_accepted = serializers.BooleanField(default=False)
    is_volunteer = serializers.BooleanField(default=False)
    role = serializers.CharField(max_length=30, allow_null=False, allow_blank=False)
    domain = serializers.CharField(max_length=30, allow_null=False, allow_blank=False)
    reason = serializers.CharField(max_length=300, allow_null=False, allow_blank=False)

    def create(self, validated_data):
        club_member = ClubMember.objects.create(**validated_data)
        return club_member


class ClubEventSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    banner = serializers.CharField(max_length=400, allow_null=False, allow_blank=False)
    name = serializers.CharField(max_length=30, allow_null=False, allow_blank=False)
    description = serializers.CharField(
        max_length=200, allow_null=False, allow_blank=False
    )
    of_club = ClubSerializer(read_only=True, many=False)
    start_date = serializers.DateField(allow_null=False)
    end_date = serializers.DateField(allow_null=False)
    no_of_registrations = serializers.IntegerField(allow_null=False, default=0)
    registration_status = serializers.CharField(max_length=20, allow_null=False)
    registration_left = serializers.IntegerField(allow_null=False, default=0)


class EventRegistrationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    of_event = ClubEventSerializer(read_only=True)
    registration_for_user = UserSerializer(read_only=True)
    registering_user_email = serializers.EmailField(
        max_length=30, allow_null=False, allow_blank=False
    )
