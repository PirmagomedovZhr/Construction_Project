from django.contrib import admin
from .models import Project, User, ProjectUser, TimeSpent, ProjectFile

admin.site.register(Project)
admin.site.register(User)
admin.site.register(ProjectUser)
admin.site.register(TimeSpent)
admin.site.register(ProjectFile)

