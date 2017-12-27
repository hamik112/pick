from django.conf.urls import url
from fb_ad_account import views

urlpatterns = [
    url(r'^$', views.FbAdAccountList.as_view()),
    url(r'^(?P<fb_account_id>[-\w]+)/check_pixel$', views.FbAdAccountPixelCheck.as_view()),
    url(r'^(?P<fb_account_id>[-\w]+)/account_category', views.FbAdAccountCategory.as_view()),
    # url(r'^(?P<fb_account_id>[-\w]+)/pixel_mappings', views.FbAdAccountPixelMapping.as_view())
]
