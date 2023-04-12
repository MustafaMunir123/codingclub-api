from rest_framework.views import APIView
from rest_framework.views import status
from codingclub_api.apps.services import (
    store_image_get_url,
    convert_to_id
)
from codingclub_api.apps.utils import success_response
from codingclub_api.apps.posts.models import Post
from codingclub_api.apps.clubs.models import Category
from codingclub_api.apps.posts.api.v1.serializers import PostSerializer
# Create your views here.


class PostApiView(APIView):

    @staticmethod
    def set_id(model, unique_param, validate_data):
        obj = model.objects.get(title=unique_param)
        validate_data['id'] = obj.id
        return validate_data

    @staticmethod
    def get_serializer():
        return PostSerializer

    def post(self, request):
        try:
            banner = request.data.pop('banner')
            print(type(request.data["tag"]))
            category = {'tags': request.data.pop("tag")[0]}
            request.data["banner"] = store_image_get_url(image_file=banner[0], path="posts/banner/")
            serializer = self.get_serializer()
            serializer = serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            self.set_id(model=Post, unique_param=serializer.validated_data["title"], validate_data=serializer.validated_data)

            post = Post.objects.get(id=serializer.validated_data["id"])
            category_ids = convert_to_id(dictionary_list=category, ManyToManyModel=Category)
            post.tag.add(*category_ids)
            post.save()
            return success_response(status=status.HTTP_200_OK, data=serializer.validated_data)
        except Exception as ex:
            raise ex
