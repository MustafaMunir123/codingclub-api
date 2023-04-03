import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from codingclub_api.apps.users.constants import PROFILE_PIC_ICON
from codingclub_api.apps.users.constants import USER_GENDER
# Create your models here.


class User(AbstractUser):
    groups = None
    user_permissions = None
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    gender = models.CharField(max_length=10, choices=USER_GENDER)
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_lead = models.BooleanField(default=False)
    phonenumber = PhoneNumberField(null=True, unique=True)
    profile_pic = models.CharField(max_length=400, default=PROFILE_PIC_ICON)
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}-{self.username}"

