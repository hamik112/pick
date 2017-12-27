from django.conf.urls import url
from neo_db import views

urlpatterns = [
    url(r'^get_advertisers$', views.get_neo_advertisers),
    url(r'^get_accounts$', views.get_neo_accounts),
    # url(r'^(?P<fb_account_id>[0-9]+)/advertisers', views.FbAdAccountCategory.as_view()),
]
