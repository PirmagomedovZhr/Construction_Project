from django.contrib import admin
from .models import Task, User, ProjectUser

admin.site.register(Task)
admin.site.register(User)
admin.site.register(ProjectUser)


