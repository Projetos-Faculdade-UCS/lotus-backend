from django.urls import include, path
from rest_framework.routers import DefaultRouter

from lotus.views import ComputadoresViewSet, ImpressorasViewSet, MonitorViewSet

router = DefaultRouter()
router.register(r"computadores", ComputadoresViewSet, basename="computadores")
router.register(r"impressoras", ImpressorasViewSet, basename="impressoras")
router.register(r"monitores", MonitorViewSet, basename="monitores")

urlpatterns = [
    path("", include(router.urls)),
]
