import uuid
from django.db import models
from codingclub_api.apps.users.models import User
from codingclub_api.apps.clubs.enums import EventStatus
from codingclub_api.apps.clubs.constants import EVENT_STATUS


# Create your models here.


class Category(models.Model):
    objects = None
    tags = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.tags

    class Meta:
        verbose_name_plural = "Categories"


class ClubDomain(models.Model):
    objects = None
    domain = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.domain


class ClubRole(models.Model):
    objects = None
    role = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.role


class Club(models.Model):
    objects = None
    logo = models.CharField(max_length=400, null=False, blank=False)
    banner = models.CharField(max_length=400, null=False, blank=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=40, null=False, blank=False, unique=True)
    description = models.CharField(max_length=200, blank=False, null=False)
    lead_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="lead_user")
    role = models.ManyToManyField(ClubRole, related_name='roles')
    domain = models.ManyToManyField(ClubDomain, related_name='domains')
    category = models.ManyToManyField(Category, related_name="category")
    is_accepted = models.BooleanField(default=False, null=True)
    rejected = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name


class ClubMember(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="club")
    is_accepted = models.BooleanField(default=False)
    is_volunteer = models.BooleanField(default=False)
    role = models.CharField(max_length=30, null=False, blank=False)
    domain = models.CharField(max_length=30, null=False, blank=False)
    reason = models.CharField(max_length=300, blank=False, null=False)

    def __str__(self):
        return f"{self.user} {self.club}"


class ClubRule(models.Model):
    rule = models.CharField(max_length=200, null=False)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="rule_club")

    def __str__(self):
        return f"{self.rule}      {str(self.club).upper()}"


class ClubEvent(models.Model):
    objects = None
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    banner = models.CharField(max_length=400, null=False, blank=False)
    name = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    of_club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="of_club")
    start_date = models.DateField(default="2023-3-4")
    end_date = models.DateField(default="2023-3-4")
    no_of_registrations = models.IntegerField(null=False, default=0, blank=False)
    registration_status = models.CharField(max_length=20, null=False, default=EventStatus.UPCOMMING.value, choices=EVENT_STATUS)
    registration_left = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return f"{self.name}  {self.of_club}"

# Deprecated
# class EventGoing(models.Model):
#     event = models.OneToOneField(ClubEvent, on_delete=models.CASCADE, related_name="event")
#     going = models.ManyToManyField(User, related_name="going")
#
#     def __str__(self):
#         return self.event


class EventRegistrations(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    of_event = models.ForeignKey(ClubEvent, on_delete=models.CASCADE, related_name="of_delete")
    registration_for_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="registration_for_user")
    registering_user_email = models.CharField(max_length=30, null=False, blank=False)

