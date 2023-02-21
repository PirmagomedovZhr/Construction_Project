from django.urls import path
from .views import (SignInView, SignUpView, logout_user, inactive_users, activate_user, Get_User, base, form,lll, kkk, jjj, user_list, user_projects)

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
    path('user/<int:user_id>/projects/', user_projects, name='user_projects'),
]