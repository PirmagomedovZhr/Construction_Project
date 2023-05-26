from django.urls import path
from .views import (project_treports, archive, archive_project, project_reports, projectt_details, projects, deletes_project, SignInView, SignUpView, logout_user, inactive_users, activate_user, Get_User, base, form, user_list, user_projects, delete_project, add_time, time_spent_list)

urlpatterns = [
    path('', base, name='base'),
    path('form/', form, name='form'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', logout_user, name='logout'),
    path('activate/', inactive_users, name='activate'),
    path('activate_user/<int:user_id>/', activate_user, name='activate_user'),
    path('use/', Get_User, name='use'),
    path('users/', user_list, name='user_list'),
    path('user_projects/<int:user_id>/', user_projects, name='user_projects'),
    path('delete_project/<int:projectuser_id>/', delete_project, name='delete_project'),
    path('add_time/<int:project_id>/', add_time, name='add_time'),
    path('timespent/', time_spent_list, name='timespent'),
    path('deletes_project/<int:project_id>/', deletes_project, name='deletes_project'),
    path('projects/', projects, name='projects'),
    path('projectt/<int:project_id>/', projectt_details, name='projectt_details'),
    path('project-reports/<int:project_id>/',project_reports, name='project_reports'),
    path('projectttt/<int:project_id>/archive/', archive_project, name='archive_project'),
    path('archived_projects/', archive, name='archived_projects'),
    path('archive/project_reports/<int:project_id>/', project_treports, name='archive_project_reports'),
]