from django.contrib import admin
from .models import Task, Profile, UserProfile

admin.site.register(Task)
admin.site.register(Profile)
admin.site.register(UserProfile)

