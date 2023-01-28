from django.contrib import admin
from .models import Task, UserProfile

admin.site.register(Task)
# Register your models here.
admin.site.register(UserProfile)
