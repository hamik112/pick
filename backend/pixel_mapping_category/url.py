from django.conf.urls import url
from pixel_mapping_category import views

urlpatterns = [
    url(r'^$', views.PixelMappingCategoryView.as_view()),
]
