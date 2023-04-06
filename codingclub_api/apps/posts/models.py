import uuid
from django.db import models
from codingclub_api.apps.users.models import User
from codingclub_api.apps.clubs.models import Category


# Create your models here.


class Post(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, null=False, primary_key=True)
    title = models.CharField(max_length=60, null=False, blank=False)
    description = models.CharField(max_length=60, null=False, blank=False)
    banner = models.CharField(max_length=400, null=False, blank=False)
    like = models.IntegerField(default=0, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    tag = models.ManyToManyField(Category, related_name="tag")
    is_accepted = models.BooleanField(null=False, default=False)
    rejected = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f"{self.title} by {self.author.name}"


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, null=False, primary_key=True)
    description = models.CharField(blank=True, max_length=50)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")

    def __str__(self):
        return f"{str(self.description)[10]}... by {self.comment_author.name}"

