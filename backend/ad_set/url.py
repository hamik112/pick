from django.conf.urls import url
from ad_set import views

urlpatterns = [
    url(r'^$', views.AdSetDetail.as_view()),
    url(r'^all$', views.AdSetAll.as_view())
]
