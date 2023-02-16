from django.urls import path
from .views import (SignInView, SignUpView, logout_user, inactive_users, activate_user, Get_User, base, form,lindex, kkk)

urlpatterns = [
    path('', base),
    path('form/', form, name='form'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', logout_user, name='logout'),
    path('activate/', inactive_users, name='activate'),
    path('activate_user/<int:user_id>/', activate_user, name='activate_user'),
    path('users/', Get_User, name='users'),
    path('lll/', lindex, name='lll'),
    path('kkk/', kkk, name='kkk'),
]