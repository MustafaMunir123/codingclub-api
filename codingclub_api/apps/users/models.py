import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Category(models.Model):
    tags = models.CharField(max_length=40)

    def __str__(self):
        return self.tags

    class Meta:
        verbose_name_plural = "Categories"


class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_lead = models.BooleanField(default=False)
    phonenumber = PhoneNumberField(null=True, unique=True)
    profile_pic = models.CharField(max_length=400, default="https://firebasestorage.googleapis.com/v0/b/schoolmanagement-api-df5f5.appspot.com/o/coding_club-api%2Fmedia%2Fprofile_pic%2Fprofile-icon.jpg?alt=media&token=95653be4-0f70-4403-8827-d60560c59d92")
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.email} {self.first_name}___{self.email}"


class Club(models.Model):
    logo = models.ImageField(upload_to="clubs/logo", null=False, blank=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=40, null=False, blank=False, unique=True)
    description = models.CharField(max_length=200, blank=False, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="lead_user")
    category = models.ManyToManyField(Category, related_name="category")

    def __str__(self):
        return self.name


class ClubMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user")
    club = models.ForeignKey(Club, on_delete=models.PROTECT, related_name="club")
    is_accepted = models.BooleanField(default=False)
    is_volunteer = models.BooleanField(default=False)
    role = models.CharField(max_length=30, null=False, blank=False)
    domain = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return f"{self.user}"


class ClubRule(models.Model):
    rule = models.CharField(max_length=200, null=False)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="rule_club")

    def __str__(self):
        return f"{self.rule}      {str(self.club).upper()}"


class ClubEvent(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="event_club")

    def __str__(self):
        return f"{self.name}  {self.club}"
