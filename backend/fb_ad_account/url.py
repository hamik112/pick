from django.conf.urls import url
from fb_ad_account import views

urlpatterns = [
    url(r'^$', views.FbAdAccountList.as_view()),
    url(r'^confirm_ad_account$', views.CheckAccountId.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.FbAdAccountDetail.as_view()),
    url(r'^accounts_by_category$', views.FbAdAccountListByCategory.as_view()),
    url(r'^ad_account_pixel_events$', views.AccountPixelEvent.as_view()),
    url(r'^pixel_events$', views.PixelEvent.as_view()),
    url(r'^ad_account_pixels$', views.AccountPixel.as_view()),
    # url(r'^(?P<act_account_id>[-\w]+)/ad_account_id', views.FbAdAccountPixelCheck.as_view()),
    # url(r'^(?P<act_account_id>[-\w]+)/check_pixel$', views.FbAdAccountPixelCheck.as_view()),
    url(r'^(?P<act_account_id>[-\w]+)/account_category', views.FbAdAccountCategory.as_view()),
    url(r'^(?P<fb_account_id>[-\w]+)/default_target', views.FbAdAccountDefaultTarget.as_view())
    # url(r'^(?P<fb_account_id>[-\w]+)/pixel_mappings', views.FbAdAccountPixelMapping.as_view())
]
