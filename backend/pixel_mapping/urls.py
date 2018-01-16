from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.PixelMappingViewSet)

urlpatterns = [
    # url(r'', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.PixelMappingView.as_view()),
    url(r'^default$', views.PixelMappingView.as_view()),


]
