"""pickdata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.views import serve

from fb_ad_account import url as fb_ad_account_urls
from neo_db import url as neo_db_urls
from user import url as url_urls
from ad_set import url as ad_set_urls
from ad_set_insight import url as ad_set_insight_urls

urlpatterns = [
    url(r'^$', serve, kwargs={'path': 'index.html'}),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^fb_ad_accounts/', include(fb_ad_account_urls)),
    url(r'^neo_db/', include(neo_db_urls)),
    url(r'^users/', include(url_urls)),
    url(r'^ad_sets/', include(ad_set_urls)),
    url(r'^ad_set_insights/', include(ad_set_insight_urls))
]
