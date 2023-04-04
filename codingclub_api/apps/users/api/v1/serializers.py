from rest_framework import serializers
from codingclub_api.apps.users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        # print(instance)
        user = User.objects.filter(user_id=instance.user_id).update(**validated_data)
        return user


