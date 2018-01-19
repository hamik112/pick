from django.conf.urls import url
from neo_account import views

urlpatterns = [
    url(r'^$', views.NeoAccountView.as_view()),
]
