from django.contrib import admin
from codingclub_api.apps.users.models import User, Club, ClubMember, Category, ClubRule, ClubEvent

# Register your models here.
admin.site.register(Category)
admin.site.register(Club)
admin.site.register(ClubMember)
admin.site.register(ClubRule)
admin.site.register(ClubEvent)


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'profile_pic']


admin.site.register(User, UserAdmin)

