from django.urls import include, path
from rest_framework.routers import DefaultRouter

from lotus.views import ComputadoresViewSet

router = DefaultRouter()
router.register(r"computadores", ComputadoresViewSet, basename="computadores")

urlpatterns = [
    path("", include(router.urls)),
]
