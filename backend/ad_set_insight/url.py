from django.conf.urls import url
from ad_set_insight import views

urlpatterns = [
    url(r'^$', views.AdSetInsightByAccount.as_view()),
]
