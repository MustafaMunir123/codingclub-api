from rest_framework import serializers
from codingclub_api.apps.posts.models import Post
from codingclub_api.apps.users.api.v1.serializers import UserSerializer
from codingclub_api.apps.clubs.api.v1.serializers import CategorySerializer


class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=60, allow_null=False, allow_blank=False)
    description = serializers.CharField(max_length=60, allow_null=False, allow_blank=False)
    banner = serializers.CharField(max_length=400, allow_null=False, allow_blank=False)
    like = serializers.IntegerField(default=0, allow_null=False)
    author_id = serializers.CharField(max_length=40, allow_null=True)
    tag = CategorySerializer(read_only=True, many=True)
    is_accepted = serializers.BooleanField(allow_null=False, default=False)
    rejected = serializers.BooleanField(allow_null=False, default=False)

    def create(self, validated_data):
        print(validated_data)
        post = Post.objects.create(**validated_data)
        return post
