from django.contrib import admin
from .models import User, Profile, Job, Application
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

admin.site.register(Profile)
admin.site.register(Job)
admin.site.register(Application)
