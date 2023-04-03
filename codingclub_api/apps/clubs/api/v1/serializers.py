from rest_framework import serializers
from codingclub_api.apps.clubs.models import Club, ClubMember
from codingclub_api.apps.users.models import User
from codingclub_api.apps.users.api.v1.serializers import UserSerializer


class CategorySerializer(serializers.Serializer):
    tags = serializers.CharField(max_length=40)


class ClubRoleSerializer(serializers.Serializer):
    role = serializers.CharField(max_length=40)


class ClubDomainSerializer(serializers.Serializer):
    domain = serializers.CharField(max_length=40)


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

    def create(self, validated_data):
        club = Club.objects.create(**validated_data)
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
