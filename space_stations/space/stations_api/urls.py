from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import StationViewSet


router = SimpleRouter()
router.register('stations', StationViewSet, basename='stations')

urlpatterns = [
    #path('stations/<int: station_id>/state/')
    path('', include(router.urls))
]
