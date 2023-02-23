from django.urls import path
from .views import (SignInView, SignUpView, logout_user, inactive_users, activate_user, Get_User, base, form,lll, kkk, jjj, user_list, user_projects, delete_project, my_projects)

urlpatterns = [
    path('', base),
    path('form/', form, name='form'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', logout_user, name='logout'),
    path('activate/', inactive_users, name='activate'),
    path('activate_user/<int:user_id>/', activate_user, name='activate_user'),
    path('use/', Get_User, name='use'),
    path('lll/', lll, name='lll'),
    path('jjj/', jjj, name='jjj'),
    path('kkk/', kkk, name='kkk'),
    path('users/', user_list, name='user_list'),
    path('user_projects/<int:user_id>/', user_projects, name='user_projects'),
    path('delete_project/<int:project_id>/', delete_project, name='delete_project'),
    path('my-projects/', my_projects, name='my_projects'),

]