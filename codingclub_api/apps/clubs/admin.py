from django.contrib import admin
from codingclub_api.apps.clubs.models import(
    Club,
    ClubMember,
    Category,
    ClubRule,
    ClubEvent,
    ClubRole,
    ClubDomain,
    EventGoing
)

# Register your models here.

admin.site.register(Category)
admin.site.register(Club)
admin.site.register(ClubMember)
admin.site.register(ClubRule)
admin.site.register(ClubEvent)
admin.site.register(ClubRole)
admin.site.register(ClubDomain)
admin.site.register(EventGoing)
