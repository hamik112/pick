from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.PickdataAccountTargetViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^targetpick', views.TargetPick.as_view()),
    url(r'^custom_target$', views.CustomTarget.as_view()),
    url(r'^target_chart$', views.TargetChart.as_view())
]
