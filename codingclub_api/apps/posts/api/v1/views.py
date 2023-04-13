from rest_framework.views import APIView, status

from codingclub_api.apps.clubs.models import Category
from codingclub_api.apps.posts.api.v1.serializers import PostSerializer
from codingclub_api.apps.posts.models import Post
from codingclub_api.apps.services import convert_to_id, store_image_get_url
from codingclub_api.apps.typings import SuccessResponse
from codingclub_api.apps.utils import success_response

# Create your views here.


class PostApiView(APIView):
    @staticmethod
    def set_id(model, unique_param, validate_data) -> None:
        obj = model.objects.get(title=unique_param)
        validate_data["id"] = obj.id

    @staticmethod
    def get_serializer():
        return PostSerializer

    def post(self, request) -> SuccessResponse:
        try:
            banner = request.data.pop("banner")
            category = {"tags": request.data.pop("tag")[0]}
            request.data["banner"] = store_image_get_url(
                image_file=banner[0], path="posts/banner/"
            )
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            self.set_id(
                model=Post,
                unique_param=serializer.validated_data["title"],
                validate_data=serializer.validated_data,
            )

            post = Post.objects.get(id=serializer.validated_data["id"])
            category_ids = convert_to_id(
                dictionary_list=category, ManyToManyModel=Category
            )
            post.tag.add(*category_ids)
            post.save()
            return success_response(
                status=status.HTTP_200_OK, data=serializer.validated_data
            )
        except Exception as ex:
            raise ex

    def get(self, request, pk=None) -> SuccessResponse:
        serializer = self.get_serializer()
        if pk is not None:
            post = Post.objects.get(id=pk, is_accepted=True)
            serializer = serializer(post)
            print(post)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        posts = Post.objects.filter(is_accepted=True)
        serializer = serializer(posts, many=True)
        return success_response(status=status.HTTP_200_OK, data=serializer.data)


class PostLikeApiView(APIView):
    @staticmethod
    def like(request, pk) -> SuccessResponse:
        try:
            post = Post.objects.get(id=pk)
            post.like += 1
            post.save()
            serializer = PostSerializer(post)
            return success_response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as ex:
            raise ex

    def post(self, request, pk=None) -> SuccessResponse:
        if "like" in request.path:
            return self.like(request, pk)
