from django.urls import path
from . import views
from .views import (SignInView, SignUpView, logout_user, get_user)

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('form/', views.form, name='form'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', logout_user, name='logout'),
    path('users/', get_user, name='users'),

]