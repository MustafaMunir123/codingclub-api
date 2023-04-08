from django.contrib import admin
from codingclub_api.apps.users.models import User, OTP

# Register your models here.

admin.site.register(OTP)


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'profile_pic']


admin.site.register(User, UserAdmin)

