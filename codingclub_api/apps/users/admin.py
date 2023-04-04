from django.contrib import admin
from codingclub_api.apps.users.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'profile_pic']


admin.site.register(User, UserAdmin)

