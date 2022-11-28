from django.urls import path
from . import views
from .views import (SignInView, SignUpView)

urlpatterns = [
    path('', views.index),
    path('about-us', views.about),
    path('form', views.form),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
]
