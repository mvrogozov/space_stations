from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import StationViewSet

router = SimpleRouter()
router.register('stations', StationViewSet, basename='stations')

urlpatterns = [
    path('', include(router.urls))
]
