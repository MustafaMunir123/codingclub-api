from django.contrib import admin
from codingclub_api.apps.competitions.models import Competitor, Competition

# Register your models here.

admin.site.register(Competitor)
admin.site.register(Competition)
