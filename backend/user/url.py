from django.conf.urls import url, include
from rest_framework import routers
from user import views

urlpatterns = [
    url(r'^me$', views.Me.as_view()),
    url(r'^signin$', views.Signin.as_view()),
    url(r'^signout$', views.Signout.as_view()),
]
