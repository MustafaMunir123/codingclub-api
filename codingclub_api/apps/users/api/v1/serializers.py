from rest_framework import serializers
from codingclub_api.apps.users.models import User
from drf_extra_fields.fields import Base64ImageField


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

