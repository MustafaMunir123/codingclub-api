import uuid
from django.db import models

# from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Competitor(models.Model):
    objects = None
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    ranking = models.IntegerField(null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False, unique=True)
    # competition = models.ForeignKey(Competition, on_delete=models.CASCADE ,related_name="competitors")
    # phonenumber = PhoneNumberField(null=)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Competition(models.Model):
    objects = None
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=70, null=False, blank=False, unique=True)
    organized_by = models.CharField(max_length=70, null=False, blank=False)
    is_active = models.BooleanField(default=True, null=False, blank=False)
    competitor = models.ManyToManyField(Competitor, related_name="competitor")

    def __str__(self):
        return f"{self.name} -{self.organized_by}"
